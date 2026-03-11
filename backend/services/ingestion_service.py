from modulos.db import supabase

class IngestionService:
    @staticmethod
    def save_asset_metadata(project_id: str, asset_type: str, original_name: str, storage_path: str = "pending_bucket"):
        try:
            res = supabase.table("brand_assets").insert({
                "project_id": project_id,
                "asset_type": asset_type,
                "original_name": original_name,
                "storage_path": storage_path
            }).execute()
            return res.data
        except Exception as e:
            raise Exception(f"Falla en el registro: {e}")
