import requests

url_post = "http://localhost:4001/db/execute?"
url_get = "http://localhost:4001/db/query?"
headers = {'Content-type' : 'application/json'}
election_data = '["CREATE TABLE ElectionName (election_id INTEGER not null PRIMARY KEY, election_name text, DateOfCreation text, DateOfStart Text DEFAULT ' + "'NOT STARTED'" + ')", "Drop TABLE test","CREATE TABLE CandidatesName (candidate_id INTEGER not null, candidate_name text, votes INTEGER DEFAULT 0, election_id text, FOREIGN KEY (election_id) REFERENCES ElectionName(election_id))"]'
response = requests.post(url = url_post, data = election_data,  headers = headers)

while True:

    select = {'q' : 'SELECT * FROM ElectionName'}
    response = requests.get(url = url_get, params = select, headers = headers)
    einfo = response.json()['results'][0]

    if 'values' in einfo:
        einfo = einfo['values']
        print("Voting Machine:\n1.Create Election\n2.Choose Election(to vote)\n3.Election Status")
        id1 = input("Enter id: ")
        print()
        if id1 == '1':
            while True:
                name = input("Enter Election Name: ")
                check = False
                for i in range(0 , len(einfo)):
                    if name == einfo[i][1]:
                        check = True
                        print("Name already in use.\n")
                        print("Names in use:")
                        for i in range(0, len(einfo)):
                            print(i + 1, '. ', einfo[i][1], sep = '' )
                if not check:
                    break


            select = {'q': 'SELECT MAX(election_id) FROM ElectionName'}
            response = requests.get(url = url_get, params = select, headers = headers)
            election_id = str(response.json()['results'][0]['values'][0][0])
            while True:
                cno = input("Enter number of candidates: ")
                if cno.isdigit() and cno != '0':
                    cno = int(cno)
                    break
                elif cno == '0':
                    print("0 is not a valid number for candidates")
                else:
                    print("Not a valid number")
            candidate_name = []
            count = 0
            while count < cno:
                cnam = input("Enter candidate name: ").rstrip()
                if cnam != " " and cnam != '':
                    candidate_name.append(cnam)
                    count += 1
                else:
                    print("Invalid candidate_name")


            candidates_data = '["INSERT INTO CandidatesName (candidate_name, election_id, candidate_id) VALUES'

            print(name, "is created with ")
            for i in range(0, len(candidate_name)):
                print(i + 1, ". ", candidate_name[i], sep = "")
                if i != len(candidate_name) - 1:
                    candidates_data += '(\\"' + candidate_name[i] + '\\",' + election_id +  ',' + str(i + 1) + '), '
                else:
                    candidates_data += '(\\"' + candidate_name[i] + '\\",' + election_id + ',' + str(i + 1) + ')"]'
            election_data = '[ "INSERT INTO ElectionName(election_name, DateOfCreation) VALUES(\\"' + name +'\\", CURRENT_DATE)" ]'
            print(election_data)
            response = requests.post(url = url_post, data = election_data,  headers = headers)
            response = requests.post(url = url_post, data = candidates_data,  headers = headers)
            print(response.url)
            print(response.encoding)
            print(response.headers)


        elif id1 == '3' or id1 == '2':
            while True:
                print("Election Names:")
                for i in range(0, len(einfo)):
                    print(i + 1, '. ', einfo[i][1], sep = '' )
                election_id = input("Enter id: ")
                check = False
                for i in range(0 ,len(einfo)):
                    if election_id == str(einfo[i][0]):
                        select = {'q' : 'SELECT election_id, candidate_name, votes, candidate_id FROM CandidatesName Where election_id = ' + election_id}
                        response = requests.get(url = url_get, params = select, headers = headers)
                        cinfo = response.json()['results'][0]['values']
                        check = True
                        break
                    elif election_id == 'a' and id1 == '3':
                        select = {'q' : 'SELECT election_id, candidate_name, votes, candidate_id FROM CandidatesName '}
                        response = requests.get(url = url_get, params = select, headers = headers)
                        cinfo = response.json()['results'][0]['values']
                        check = True
                        break

                if not check:
                    print("Invalid id.\n")
                else:
                    break
            if id1 == '3':
                if election_id != 'a':
                    print()
                    print("Election Name:", einfo[int(election_id) - 1][1])
                    print("Date Of Creation:", einfo[int(election_id) - 1][2])
                    print("Date Of Election Start:", einfo[int(election_id) - 1][3])
                    print('Candidate Names: ')
                    for i in range(0, len(cinfo)):
                        print(i + 1, ". ", cinfo[i][1], cinfo[i][2])
                else:
                    for i in range(0, len(einfo)):
                        print()
                        print("Election Name:", einfo[i][1])
                        print("Date Of Creation:", einfo[i][2])
                        print("Date Of Election Start:", einfo[i][3])
                        print('Candidate Names: ')
                        count = 1
                        for j in range(0, len(cinfo)):
                            if int(cinfo[j][0]) == i + 1:
                                print(count, ". ", cinfo[j][1], cinfo[j][2])
                                count += 1
                        if i != len(einfo):
                            print()


            elif id1 == '2':
                while True:
                    for i in range(0, len(cinfo)):
                        print(i + 1, '. ', cinfo[i][1], sep = '' )
                    index = input("Enter id: ")
                    check = False
                    for i in range(0 ,len(cinfo)):
                        if int(index) == cinfo[i][3]:
                            check = True
                            break
                    if not check:
                        print("Invalid id.\n")
                    else:
                        break
                if einfo[int(election_id) - 1][-1] == 'NOT STARTED':
                    data = '[ "UPDATE ElectionName SET DateOfStart = CURRENT_DATE WHERE election_id =  '+ election_id + '" ]'
                    response = requests.post(url = url_post, data = data,  headers = headers)

                data = '[ "UPDATE CandidatesName SET votes = votes + 1 WHERE candidate_id = ' + index + ' AND election_id = ' + str(cinfo[int(index) - 1][0])+ '" ]'
                response = requests.post(url = url_post, data = data,  headers = headers)
                print("Thank You For Voting")

        elif id1 == '4':
            break

        else:
            print("Enter Valid id.\n")


    else:
        print("No Election Exists\nPlease Create Election")
        name = input("Enter Election Name: ")
        election_id = str(1)

        while True:
            cno = input("Enter number of candidates: ")
            if cno.isdigit() and cno != '0':
                cno = int(cno)
                break
            elif cno == '0':
                print("0 is not a valid number for candidates")
            else:
                print("Not a valid number")

        candidate_name = []
        count = 0
        while count < cno:
            cnam = input("Enter candidate name: ").rstrip()
            if cnam != " " and cnam != '':
                candidate_name.append(cnam)
                count += 1
            else:
                print("Invalid candidate_name")
        candidates_data = '["INSERT INTO CandidatesName (candidate_name, election_id, candidate_id) VALUES'

        for i in range(0, len(candidate_name)):
            if i != len(candidate_name) - 1:
                candidates_data += '(\\"' + candidate_name[i] + '\\",' + election_id +  ',' + str(i + 1) + '), '
            else:
                candidates_data += '(\\"' + candidate_name[i] + '\\",' + election_id + ',' + str(i + 1) + ')"]'
        election_data = '[ "INSERT INTO ElectionName(election_name, DateOfCreation) VALUES(\\"' + name +'\\", CURRENT_DATE)" ]'
        response = requests.post(url = url_post, data = election_data,  headers = headers)

        response = requests.post(url = url_post, data = candidates_data,  headers = headers)
        print("Election has been made.")
    print()
print("Thank You")
#select = {'q':"SELECT * FROM   FOO"}
#response = requests.get(url = url, params = select, headers = headers)

