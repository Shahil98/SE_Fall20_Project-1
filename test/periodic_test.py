import test.periodic as pt

uid1 = 'cdfd2609-e7aa-4dff-af50-649a89bd8805'
body = [{"uid": uid1, "file_name": "saurabh.py", "start_date": "2020-09-26 17:15:00", "end_date": "2020-09-26 19:00:00", "file_type": ".py"}]
code = pt.tester(body)
assert code == 200
code = pt.tester_tester()
assert code == 200
