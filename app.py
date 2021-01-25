from settings import *
from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.register_default(
   metrics.counter(
       'by_path_counter', 'Request count by request paths',
       labels={'path': lambda: request.path}
   )
)


client = app.test_client()

engine = create_engine('postgresql://' + API_DB_USER + ':' + API_DB_PASSWORD + '@' + API_DB_HOST)

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)

log_file_path = (os.getcwd() + "/log/requests.log")
logger.add(log_file_path, format="{time} {level} {module} {message}",
           level="DEBUG", rotation="10 MB", retention="1 days", compression="zip")


@app.route('/cdr_list/<cdr_id>', methods=['GET'])
def get_list(cdr_id):
    try:
        cdr_list = CDR_Model.query.filter_by(id=cdr_id)
        serialized = []
        for cdr_string in cdr_list:
            serialized.append({
                'id': cdr_string.id,
                'Local_Time': cdr_string.Local_Time,
                'CDR_Type': cdr_string.CDR_Type,
                'IP_Group_Name': cdr_string.IP_Group_Name,
                'IP_Profile_Name': cdr_string.IP_Profile_Name,
                'Call_ID': cdr_string.Call_ID,
                'Session_ID': cdr_string.Session_ID,
                'Setup_Time': cdr_string.Setup_Time,
                'Connect_Time': cdr_string.Connect_Time,
                'Release_Time': cdr_string.Release_Time,
                'Call_Duration': cdr_string.Call_Duration,
                'Endpoint_Type': cdr_string.Endpoint_Type,
                'Call_Originated': cdr_string.Call_Originated,
                'Source_URI': cdr_string.Source_URI,
                'Destination_URI': cdr_string.Destination_URI,
                'Termination_Side': cdr_string.Termination_Side,
                'Termination_Reason': cdr_string.Termination_Reason,
                'SIP_Termination_Reason': cdr_string.SIP_Termination_Reason,
                'SIP_Termination_Description': cdr_string.SIP_Termination_Description
            })
    except Exception as err:
        return {'message': str(err)}, 400
    else:
        logger.info('New request from: ' + str(request.remote_addr) + ' HTTP Method: ' + str(request.method))
        return jsonify(serialized)


@app.route('/cdr_list', methods=['POST'])
def update_list():
    try:
        new_one = CDR_Model(**request.json)
        session.add(new_one)
        session.commit()
        serialized = {
            'id': new_one.id,
            'Local_Time': new_one.Local_Time,
            'CDR_Type': new_one.CDR_Type,
            'IP_Group_Name': new_one.IP_Group_Name,
            'IP_Profile_Name': new_one.IP_Profile_Name,
            'Call_ID': new_one.Call_ID,
            'Session_ID': new_one.Session_ID,
            'Setup_Time': new_one.Setup_Time,
            'Connect_Time': new_one.Connect_Time,
            'Release_Time': new_one.Release_Time,
            'Call_Duration': new_one.Call_Duration,
            'Endpoint_Type': new_one.Endpoint_Type,
            'Call_Originated': new_one.Call_Originated,
            'Source_URI': new_one.Source_URI,
            'Destination_URI': new_one.Destination_URI,
            'Termination_Side': new_one.Termination_Side,
            'Termination_Reason': new_one.Termination_Reason,
            'SIP_Termination_Reason': new_one.SIP_Termination_Reason,
            'SIP_Termination_Description': new_one.SIP_Termination_Description
        }
    except Exception as err:
        logger.error('Massage: ' + str(err) + ', Receiving json data from SBC: ' + str(request.json))
        return {'Message': str(err), 'Data': str(request.json)}, 400

    else:
        logger.info('New request POST from: ' + str(request.remote_addr) + ' HTTP Method: ' +
                    str(request.method) + ' Data: ' + str(serialized))
        return {'Message': str('Done!'), 'cdr_row_num': str(serialized['id'])}, 200


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
