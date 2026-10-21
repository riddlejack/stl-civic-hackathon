"""Local server for the DoneStat prototype: the static site plus one read-only lookup.

    .venv/bin/python -I scripts/night/N6/serve.py            # runs the bridge, then serves
    .venv/bin/python -I scripts/night/N6/serve.py --no-bridge
    open http://127.0.0.1:8806/

Serves site/ on 127.0.0.1 only (nothing is published). The one dynamic route,
/api/receipt/<request number>, answers the receipt search box from N1's database
(build/stl.duckdb, view receipt_base) at block level. It returns no ids: the number
a visitor types is not echoed back, and the site's data files carry none.
This stands in for the weekly job's own lookup; on static
hosting the box explains that the lookup needs the database.
"""
import http.server
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bridge  # noqa: E402

PORT = int(os.environ.get('PORT', '8806'))
SITE = bridge.B('site')


def lookup(rid):
    if not re.fullmatch(r'\d{5,8}', rid):
        return 400, {'found': False, 'reason': 'A request number is five to eight digits.'}
    rows = bridge.q('SELECT * FROM receipt_base WHERE request_id = ?', [int(rid)])
    if rows is None:
        return 503, {'found': False, 'reason': "The weekly job's database is not available on this server."}
    if not rows:
        return 404, {'found': False, 'reason': 'No request with that number in the 311 file.'}
    r = rows[0]
    if r.get('sensitive'):
        return 200, {'found': True, 'withheld': True,
                     'reason': 'This request type (encampments, welfare checks, discrimination and legal matters) is never shown below ward level.'}
    if r.get('problem_code') in bridge.EXCLUDE_TYPES:
        pass  # a single receipt is fine; the type is only kept out of ward comparisons
    c = bridge.clean_receipt(r)
    c['timeline'] = bridge.receipt_timeline(c)
    c['line'] = bridge.receipt_line(c)
    c = bridge.strip_ids(c)
    c.pop('sensitive', None)
    c['found'] = True
    return 200, bridge.scrub_obj(c)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=SITE, **k)

    def log_message(self, fmt, *args):  # keep request numbers out of the console log
        path = re.sub(r'/api/receipt/\d+', '/api/receipt/<n>', self.path)
        sys.stderr.write(f'{self.address_string()} {self.command} {path} {args[1] if len(args) > 1 else ""}\n')

    def do_GET(self):
        if self.path.startswith('/api/receipt/'):
            code, body = lookup(self.path.rsplit('/', 1)[-1].split('?')[0])
            data = json.dumps(body, default=str, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        return super().do_GET()

    def end_headers(self):
        if not self.path.startswith('/api/'):
            self.send_header('Cache-Control', 'no-cache')
        super().end_headers()


def main():
    if '--no-bridge' not in sys.argv:
        bridge.main()
    srv = http.server.HTTPServer(('127.0.0.1', PORT), Handler)
    print(f'DoneStat prototype on http://127.0.0.1:{PORT}/  (Ctrl-C to stop)')
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
