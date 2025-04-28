from flask import jsonify

@app.route('/')
def get_table_data():
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        audiences = [224, 344, 411]

        table_data = {}
        for aud in audiences:
            cursor.execute(
                "SELECT component_type, model, status FROM components WHERE location = ?", (aud,)
            )
            devices = cursor.fetchall()

            for i, device in enumerate(devices):
                component_type, model, status = device
                device_name = f"{component_type[0]}{i + 1}-{model}"
                table_data.setdefault(aud, []).append((device_name, status))

        max_rows = max(len(table_data.get(aud, [])) for aud in audiences)

        cell_text = []
        colors = []
        for i in range(max_rows):
            row_text = []
            row_colors = []
            for aud in audiences:
                if i < len(table_data[aud]):
                    device_name, status = table_data[aud][i]
                    row_text.append(device_name)
                    if status == 'Active':
                        row_colors.append('yellow')
                    elif status == 'Free':
                        row_colors.append('lightgreen')
                    else:
                        row_colors.append('lightcoral')
                else:
                    row_text.append('')
                    row_colors.append('white')

            cell_text.append(row_text)
            colors.append(row_colors)

        col_labels = [f"P{aud}" for aud in audiences]
        return jsonify({'col_labels': col_labels, 'cell_text': cell_text, 'colors': colors})
    finally:
        if conn:
            conn.close()
