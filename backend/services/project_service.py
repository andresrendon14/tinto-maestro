from modulos.db import supabase

class ProjectService:
    @staticmethod
    def create_client_and_project(contact_name: str, company_name: str, email: str, project_name: str):
        try:
            client_res = supabase.table("clients").insert({"name": contact_name, "company_name": company_name, "email": email}).execute()
            client_data = client_res.data[0] if client_res.data else None
            if client_data:
                project_res = supabase.table("projects").insert({"client_id": client_data['id'], "name": project_name, "status": "draft", "current_stage": "onboarding"}).execute()
                return project_res.data[0] if project_res.data else None
            return None
        except Exception as e:
            raise Exception(f"Falla en la base de datos: {e}")

    @staticmethod
    def get_active_projects():
        try:
            response = supabase.table("projects").select("id, name, current_stage, clients(company_name)").execute()
            return response.data
        except Exception as e:
            return []
