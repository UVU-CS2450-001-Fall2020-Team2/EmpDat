"""TODO:
    1. Make change request class change_requests
        -id
        -user_id (author)
        -table_name
        -created_at
        -updated_at
        -approved_at NULLABLE
        -row_id
        -field_name (NULL if its the entire record)
        -field_new_value (varchar infinity)
        -reason
    2. Populate table with above values
"""
#, id, user_id, table_name, created_at, updated_at, approved_at, row_id, field_name, field_new_value, reason
class changeRequest():
    def __init__(self):
        # self.id = id
        # self.user_id = user_id
        # self.table_name = table_name 
        # self.created_at = created_at
        # self.updated_at = updated_at
        # self.approved_at = approved_at
        # self.row_id = row_id
        # self.field_name = field_name
        # self.field_new_value = field_new_value
        # self.reason = reason
        self.id = 1
        self.user_id = '11537'
        self.table_name = 3 
        self.created_at = '11/15/20'
        self.updated_at = '11/17/20'
        self.approved_at = ''
        self.row_id = 7
        self.field_name = 'Classification'
        self.field_new_value = 'Salary'
        self.reason = 'Went full-time.'
    
    def populateData(self):
        return self.id; 
        