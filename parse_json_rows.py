import pandas as pd
import simplejson as json

def parse_json_rows(df):
    """
    Expands each JSON array into multiple rows.
    1 row with 6 objects → 6 separate rows
    """
    
    all_records = []

    for idx, row in df.iterrows():
        s = row['Additional Info']  # ← your JSON column name

        try:
            # NULL check
            if s is None or str(s).strip() in ('', 'None', 'null', 'NULL'):
                continue

            # Parse JSON
            data = json.loads(str(s).strip())

            # Handle single object
            if not isinstance(data, list):
                data = [data]

            # Loop ALL objects → each becomes ONE row
            for item in data:
                new_row = {}

                # Copy ALL original columns from source row
                for col in df.columns:
                    new_row[col] = row[col]

                # Add parsed columns
                new_row['workGroup_value']    = str(item.get('workGroup', {}).get('value',    '') or '')
                new_row['workGroup_actionBy'] = str(item.get('actionBy', '') or '')
                new_row['workGroup_actionAt'] = str(item.get('actionAt', '') or '')
                new_row['user_value']         = str(item.get('user', {}).get('value',    '') or '')
                new_row['user_actionBy']      = str(item.get('user', {}).get('actionBy', '') or '')
                new_row['id']                 = str(item.get('id', '') or '')

                all_records.append(new_row)

        except Exception as e:
            # Keep original row with error info
            new_row = {}
            for col in df.columns:
                new_row[col] = row[col]
            new_row['workGroup_value']    = 'ERR:' + str(e)[:30]
            new_row['workGroup_actionBy'] = ''
            new_row['workGroup_actionAt'] = ''
            new_row['user_value']         = ''
            new_row['user_actionBy']      = ''
            new_row['id']                 = ''
            all_records.append(new_row)

    return pd.DataFrame(all_records)


def get_output_schema():
    return pd.DataFrame({
        # Original columns
        'Additional Info'    : prep_string(),

        # New expanded columns
        'workGroup_value'    : prep_string(),
        'workGroup_actionBy' : prep_string(),
        'workGroup_actionAt' : prep_string(),
        'user_value'         : prep_string(),
        'user_actionBy'      : prep_string(),
        'id'                 : prep_string()
    })