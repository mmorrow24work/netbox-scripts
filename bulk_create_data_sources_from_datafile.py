import json

from extras.scripts import Script, StringVar, BooleanVar
from core.models import DataSource, DataFile


class BulkCreateDataSourcesFromDataFile(Script):
    """
    Create/update NetBox core.DataSource objects from a JSON config file stored as a core.DataFile
    (i.e. a file synced from an existing "config" DataSource such as your GitHub repo).

    - Reads JSON from DataFile.data (BinaryField)
    - Creates/updates DataSource objects using ORM
    - Optional: sync each created/updated DataSource
    """

    class Meta:
        name = "Bulk create Data Sources from DataFile (JSON)"
        description = "Creates/updates NetBox Data Sources using a JSON file stored in a synced DataFile."

    # Defaults tailored to your environment
    config_datasource_name = StringVar(
        label="Config DataSource name",
        description="The NetBox Data Source that syncs your repo containing the JSON config file.",
        default="github",  # <-- your DataSource name from the API output
    )

    config_file_path = StringVar(
        label="Config file path inside the repo",
        description="Path relative to the Data Source root (as stored in DataFile.path).",
        default="data/datasources.json",  # <-- change if you store it elsewhere
    )

    update_existing = BooleanVar(
        label="Update existing Data Sources if names match?",
        default=True,
        description="If true, update fields on existing DataSource records with the same name.",
    )

    sync_created_or_updated = BooleanVar(
        label="Sync each created/updated Data Source now?",
        default=False,
        description="If true (and commit=True), call DataSource.sync() after create/update (can be slow).",
    )

    def run(self, data, commit):
        cfg_source_name = data["config_datasource_name"]
        cfg_path = data["config_file_path"]

        # 1) Locate the config DataSource (the one that contains datasources.json)
        try:
            cfg_ds = DataSource.objects.get(name=cfg_source_name)
        except DataSource.DoesNotExist:
            self.log_failure(
                f"Config DataSource '{cfg_source_name}' not found. Create it first (you already have one named 'github')."
            )
            return

        # 2) Locate the DataFile (synced file) by path
        try:
            df = DataFile.objects.get(source=cfg_ds, path=cfg_path)
        except DataFile.DoesNotExist:
            self.log_failure(
                f"Config file '{cfg_path}' not found as a DataFile under DataSource '{cfg_source_name}'. "
                f"Sync the DataSource, and verify the file path."
            )
            # Debug helper: list a sample of paths NetBox sees under this DataSource
            sample = list(
                DataFile.objects.filter(source=cfg_ds).order_by("path").values_list("path", flat=True)[:50]
            )
            if sample:
                self.log_info("First 50 DataFile paths under this DataSource:")
                for p in sample:
                    self.log_info(f" - {p}")
            else:
                self.log_warning("No DataFiles found under this DataSource (did the sync actually pull any files?).")
            return

        # DataFile.data is bytes; decode to string
        try:
            raw_text = df.data.decode("utf-8")
        except Exception as exc:
            self.log_failure(f"Failed to decode DataFile bytes as UTF-8: {exc}")
            return

        # 3) Parse JSON
        try:
            payload = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            self.log_failure(f"Invalid JSON in '{cfg_path}': {exc}")
            return

        items = payload.get("data_sources", [])
        if not isinstance(items, list) or not items:
            self.log_failure(f"No 'data_sources' list found (or list is empty) in '{cfg_path}'.")
            return

        # 4) Create/update DataSource objects
        created = updated = skipped = errors = 0

        for i, item in enumerate(items, start=1):
            name = item.get("name")
            ds_type = item.get("type")
            source_url = item.get("source_url")

            if not name or not ds_type or not source_url:
                errors += 1
                self.log_failure(f"[{i}] Missing required fields. Need: name, type, source_url.")
                continue

            enabled = bool(item.get("enabled", True))
            ignore_rules = item.get("ignore_rules", "") or ""
            parameters = item.get("parameters", None)  # dict or None
            sync_interval = item.get("sync_interval", None)  # optional integer per JobIntervalChoices

            # Create if missing
            obj, was_created = DataSource.objects.get_or_create(
                name=name,
                defaults={
                    "type": ds_type,
                    "source_url": source_url,
                    "enabled": enabled,
                    "ignore_rules": ignore_rules,
                    "parameters": parameters,
                    "sync_interval": sync_interval,
                },
            )

            # If it already existed, optionally update it
            if not was_created:
                if not data["update_existing"]:
                    skipped += 1
                    self.log_info(f"[{i}] Exists, skipping update: '{name}'")
                    continue

                changed = False
                desired = {
                    "type": ds_type,
                    "source_url": source_url,
                    "enabled": enabled,
                    "ignore_rules": ignore_rules,
                    "parameters": parameters,
                    "sync_interval": sync_interval,
                }

                for field, value in desired.items():
                    if getattr(obj, field) != value:
                        setattr(obj, field, value)
                        changed = True

                if not changed:
                    skipped += 1
                    self.log_info(f"[{i}] No changes needed: '{name}'")
                    continue

            # Dry-run messaging
            if not commit:
                msg = "Would create" if was_created else "Would update"
                self.log_success(f"[{i}] {msg} DataSource '{name}'")
                created += 1 if was_created else 0
                updated += 0 if was_created else 1
                continue

            # Persist when commit=True
            try:
                obj.full_clean()
                obj.save()
            except Exception as exc:
                errors += 1
                self.log_failure(f"[{i}] Failed to save '{name}': {exc}")
                continue

            if was_created:
                created += 1
                self.log_success(f"[{i}] Created DataSource '{name}'")
            else:
                updated += 1
                self.log_success(f"[{i}] Updated DataSource '{name}'")

            # Optional sync: creates/updates/deletes child DataFiles by fetching remote source
            if data["sync_created_or_updated"]:
                try:
                    obj.sync()
                    self.log_success(f"[{i}] Synced '{name}'")
                except Exception as exc:
                    self.log_warning(f"[{i}] Sync failed for '{name}': {exc}")

        self.log_info(
            f"Summary: created={created}, updated={updated}, skipped={skipped}, errors={errors}, commit={commit}"
        )
