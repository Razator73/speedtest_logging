import os
import datetime as dt

import speedtest
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from models import Server, Test


def test():
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    s.download()
    s.upload()
    return s.results.dict()


def log_server(res, db_session):
    server_data = res['server']
    server_id = int(server_data['id'])
    res_server = Server(id=server_id,
                        name=server_data['name'],
                        distance_km=server_data['d'],
                        country=server_data['country'],
                        host=server_data['host'],
                        latitude=server_data['lat'],
                        longitude=server_data['lon'],
                        sponsor=server_data['sponsor'],
                        url=server_data['url'],
                        country_code=server_data['cc'])

    if not db_session.query(Server).filter(Server.id == server_id).count():
        db_session.add(res_server)

    db_session.commit()


def log_test(res, db_session):
    db_session.add(Test(
        server_id=int(res['server']['id']),
        download_bps=res['download'],
        upload_bps=res['upload'],
        ping_ms=res['ping'],
        bytes_received=res['bytes_received'],
        bytes_sent=res['bytes_sent'],
        test_time=dt.datetime.strptime(res['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z'),
        server_latency=res['server']['latency'],
        ip=res['client']['ip'],
        latitude=float(res['client']['lat']),
        longitude=float(res['client']['lon'])
    ))
    db_session.commit()


if __name__ == '__main__':
    result = test()

    db = sa.create_engine(os.environ.get('PSQL_URL'))
    Session = sessionmaker(db)
    session = Session()

    log_server(result, session)
    log_test(result, session)

    session.close()
