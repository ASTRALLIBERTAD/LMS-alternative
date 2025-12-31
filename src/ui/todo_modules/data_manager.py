from pathlib import Path
from utils.common import load_json_file, save_json_file
import datetime
import json


class DataManager:
    
    def __init__(self, data_dir, drive_service=None):
        self.data_dir = Path(data_dir) if isinstance(data_dir, str) else data_dir
        self.drive_service = drive_service
        self.lms_root_id = self._load_lms_root_id()
        
        self.assignments_file = self.data_dir / "assignments.json"
        self.students_file = self.data_dir / "students.json"
        self.submissions_file = self.data_dir / "submissions.json"
        
        self.assignments_drive_id = None
        self.students_drive_id = None
        self.submissions_drive_id = None
    
    def _load_lms_root_id(self):
        config = load_json_file("lms_config.json", {})
        return config.get("lms_root_id")
    
    def _get_drive_file_id(self, filename):
        if not self.drive_service or not self.lms_root_id:
            return None
        
        try:
            result = self.drive_service.list_files(folder_id=self.lms_root_id, use_cache=False)
            files = result.get('files', []) if result else []
            
            for f in files:
                if f.get('name') == filename and f.get('mimeType') != 'application/vnd.google-apps.folder':
                    return f['id']
            
            return None
        except Exception as e:
            print(f"Error searching for {filename}: {e}")
            return None
    
    def _load_from_drive_or_local(self, filepath, drive_file_id_attr, default=None):
        if self.drive_service and self.lms_root_id:
            try:
                file_id = getattr(self, drive_file_id_attr)
                if not file_id:
                    file_id = self._get_drive_file_id(filepath.name)
                    setattr(self, drive_file_id_attr, file_id)
                
                if file_id:
                    content = self.drive_service.download_file_content(file_id)
                    if content:
                        return json.loads(content)
            except Exception as e:
                print(f"Error loading {filepath.name} from Drive: {e}")
        
        return load_json_file(filepath, default)
    
    def _save_to_local_and_drive(self, filepath, data, drive_file_id_attr):
        save_json_file(filepath, data)
        
        if self.drive_service and self.lms_root_id:
            temp_file = None
            try:
                temp_file = self.data_dir / f"temp_{filepath.name}"
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                file_id = getattr(self, drive_file_id_attr)
                
                if file_id:
                    try:
                        result = self.drive_service.update_file(file_id, str(temp_file))
                        if not (result and isinstance(result, dict) and result.get('id')):
                            setattr(self, drive_file_id_attr, None)
                            result = self.drive_service.upload_file(
                                str(temp_file),
                                parent_id=self.lms_root_id,
                                file_name=filepath.name
                            )
                            if result:
                                setattr(self, drive_file_id_attr, result.get('id'))
                    except Exception as update_error:
                        setattr(self, drive_file_id_attr, None)
                        result = self.drive_service.upload_file(
                            str(temp_file),
                            parent_id=self.lms_root_id,
                            file_name=filepath.name
                        )
                        if result:
                            setattr(self, drive_file_id_attr, result.get('id'))
                else:
                    result = self.drive_service.upload_file(
                        str(temp_file),
                        parent_id=self.lms_root_id,
                        file_name=filepath.name
                    )
                    if result:
                        setattr(self, drive_file_id_attr, result.get('id'))
                
            except Exception as e:
                print(f"Error syncing {filepath.name} to Drive: {e}")
            finally:
                if temp_file and temp_file.exists():
                    try:
                        temp_file.unlink()
                    except:
                        pass
    
    def sync_from_drive(self):
        synced = False
        
        if self.drive_service and self.lms_root_id:
            try:
                self.assignments_drive_id = self._get_drive_file_id('assignments.json')
                self.students_drive_id = self._get_drive_file_id('students.json')
                self.submissions_drive_id = self._get_drive_file_id('submissions.json')
                
                if self.assignments_drive_id:
                    content = self.drive_service.download_file_content(self.assignments_drive_id)
                    if content:
                        data = json.loads(content)
                        save_json_file(self.assignments_file, data)
                        synced = True
                
                if self.students_drive_id:
                    content = self.drive_service.download_file_content(self.students_drive_id)
                    if content:
                        data = json.loads(content)
                        save_json_file(self.students_file, data)
                        synced = True
                
                if self.submissions_drive_id:
                    content = self.drive_service.download_file_content(self.submissions_drive_id)
                    if content:
                        data = json.loads(content)
                        save_json_file(self.submissions_file, data)
                        synced = True
                
                if synced:
                    print("✓ Synced data from Drive")
            except Exception as e:
                print(f"Error syncing from Drive: {e}")
        
        return synced
    
    def load_assignments(self):
        assignments = self._load_from_drive_or_local(
            self.assignments_file, 
            'assignments_drive_id',
            []
        )
        
        modified = False
        for i, assignment in enumerate(assignments):
            if 'id' not in assignment:
                assignment['id'] = str(datetime.datetime.now().timestamp()) + str(i)
                modified = True
        
        if modified:
            self.save_assignments(assignments)
        
        return assignments
    
    def load_students(self):
        return self._load_from_drive_or_local(
            self.students_file,
            'students_drive_id',
            []
        )
    
    def load_submissions(self):
        return self._load_from_drive_or_local(
            self.submissions_file,
            'submissions_drive_id',
            []
        )
    
    def save_assignments(self, assignments):
        self._save_to_local_and_drive(
            self.assignments_file,
            assignments,
            'assignments_drive_id'
        )
    
    def save_students(self, students):
        self._save_to_local_and_drive(
            self.students_file,
            students,
            'students_drive_id'
        )
    
    def save_submissions(self, submissions):
        self._save_to_local_and_drive(
            self.submissions_file,
            submissions,
            'submissions_drive_id'
        )