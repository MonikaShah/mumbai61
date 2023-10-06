from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask, request, jsonify, abort
from sqlalchemy import text

app = Flask(__name__)
CORS(app)

# Configure your database connection here
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/mumbai61'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://divyang:CIFdVN48INeZ7K10wxvz4ZXWsMGIIFxi@dpg-cimohap5rnurtfcrk9kg-a.singapore-postgres.render.com/nowaste'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def home():
    return '''
    <h1>Welcome to the NoWaste API!</h1>
    <p>You can make a GET request to <b><code>/api</code></b> with the following parameters:</p>
    <ul>
        <li><b><code>admin_level</code></b>: <b>Mandatory</b>. Can be "ward", "prabhag", "region", or "building".</li>
        <li><b><code>sampling_period</code></b>: <b>Mandatory</b>. Can be "daily", "monthly", or "yearly".</li>
        <li><b><code>from_date</code></b>: <b>Mandatory</b>. Date in the format "YYYY-MM-DD". Must be between 2020-01-01 and 2023-06-31.</li>
        <li><b><code>to_date</code></b>: <b>Mandatory</b>. Date in the format "YYYY-MM-DD". Must be between 2020-01-01 and 2023-06-31.</li>
        <li><b><code>parent_id</code></b>: <b>Optional</b>. Integer greater than or equal to 1.</li>
    </ul>
    '''


@app.route('/api', methods=['GET'])
def get_data():
    admin_level = request.args.get('admin_level')
    sampling_period = request.args.get('sampling_period')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    parent_id = request.args.get('parent_id')

    # Check if mandatory parameters are provided
    if not all([admin_level, sampling_period, from_date, to_date]):
        return jsonify({'error': 'Missing mandatory parameters'}), 400

    # Check if admin_level and sampling_period are valid
    valid_admin_levels = ['ward', 'prabhag', 'region', 'building']
    valid_sampling_periods = ['daily', 'monthly', 'yearly']
    if admin_level not in valid_admin_levels or sampling_period not in valid_sampling_periods:
        return jsonify({'error': 'Invalid admin_level or sampling_period'}), 400

    # Check if from_date and to_date are within the valid range
    try:
        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    if not (datetime(2020, 1, 1).date() <= from_date_obj <= datetime(2023, 6, 30).date()) or \
            not (datetime(2020, 1, 1).date() <= to_date_obj <= datetime(2023, 6, 30).date()):
        return jsonify({'error': 'from_date and to_date must be between 2020-01-01 and 2023-06-30'}), 400

    # Check if parent_id is a positive integer
    if parent_id:
        try:
            parent_id = int(parent_id)
            if parent_id < 1:
                raise ValueError
        except ValueError:
            return jsonify({'error': 'parent_id must be an integer greater than or equal to 1'}), 400

    # Construct the table name
    table_name = f"{admin_level}_{sampling_period}"

    # Construct the query
    query = f"SELECT * FROM {table_name} WHERE date BETWEEN :from_date AND :to_date"
    params = {'from_date': from_date, 'to_date': to_date}

    # If parent_id is provided, add it to the query
    if parent_id:
        query += " AND parent_id = :parent_id"
        params['parent_id'] = parent_id


    # Execute the query
    try:
        result = db.session.execute(text(query), params)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Convert the result to a list of dictionaries
    # Convert the result to a list of dictionaries
    data = []
    for row in result:
        row_dict = row._asdict()
        row_dict['date'] = row_dict['date'].strftime('%Y-%m-%d')
        row_dict['population'] = str(row_dict['population'])  # Convert population to string
        data.append(row_dict)

    # Check if data is empty
    if not data:
        return jsonify({'message': 'No data found for the given parameters'}), 404

    return jsonify(data)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Invalid route'}), 404


if __name__ == '__main__':
    app.run(debug=True)
