import csv
import openpyxl
import os

class FileParser:
    @staticmethod
    def parse_csv(file_path):
        results = []
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                results.append(row)
        return results

    @staticmethod
    def parse_excel(file_path):
        results = []
        workbook = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        sheet = workbook.active
        try:
            # Assume first row is header
            headers = [cell.value for cell in sheet[1]]

            for row in sheet.iter_rows(min_row=2, values_only=True):
                if any(row): # Skip empty rows
                    results.append(dict(zip(headers, row)))
            return results
        finally:
            workbook.close()

    @staticmethod
    def validate_marks_data(data):
        required_fields = ['usn', 'subject_code', 'internal_marks', 'external_marks', 'semester', 'academic_year']
        errors = []
        
        for i, row in enumerate(data):
            # Check fields
            for field in required_fields:
                if field not in row or row[field] in (None, ''):
                    errors.append(f"Row {i+2}: Missing field {field}")
            
            # Check numeric marks
            try:
                if row.get('internal_marks') not in (None, ''):
                    float(row['internal_marks'])
                if row.get('external_marks') not in (None, ''):
                    float(row['external_marks'])
                if row.get('semester') not in (None, ''):
                    int(row['semester'])
            except (TypeError, ValueError):
                errors.append(f"Row {i+2}: Marks and semester must be numeric")
                
        return errors
