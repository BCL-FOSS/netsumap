from flask import jsonify
from init_app import app

db = app.config['DB_CONN']
main_network = app.config['NETWORK_OBJ']
probe = app.config['PROBE_OBJ']
core_conn = app.config['CORE_CONN']

# Probe Data
probe_id, hostname = probe.gen_probe_register_data()
external_ip = main_network.get_public_ip()
ports = main_network.open_tcp_ports()
   
@app.post('/probe_init')
def probe_init():
    db.ping_db()
    print('Checking probe config status...', flush=True)

    id_match = 'prb*'
    db_query_result = db.get_all_data(id_match)
    if db_query_result is not None:
        print('Probe already configured', flush=True)
        pass
    else:  
        data_values = {
                    "id": probe_id,
                    "hst_nm": hostname,
                    "ip": external_ip,
                    "ports": str(ports)
                }

        db_upload = db.upload_db_data(id=probe_id, data=data_values)
        if db_upload:
            print(db_upload, flush=True)
            db_query_value = db.get_obj_data(key=probe_id)
            if db_query_value:
               print(db_query_value, flush=True)
            else:
                return {"error":"probe registration failed"}

@app.errorhandler(404)
def page_not_found():
    return jsonify({"error": "Resource not found or does not exist"}), 404

@app.errorhandler(500)
def handle_internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

def run() -> None:
    app.run()