import requests
import configparser
import socket

class post_election_details():
    def __init__(self, config):

        config = config['rqlite']
        self.ip = config['ip']
        self.port = config['port']
        self.url_post = 'http://' + self.ip + ':' + self.port + '/db/execute?'

        self.headers = {'Content-type' : 'application/json'}

    def post(self, command_id = 4, election_id = '0', candidate_id = 0, candidate_list = [], election_name = ''):
        tables = ["ElectionName", "CandidatesName"]
        if command_id != 0 and command_id != 1:
            return "Error function does not satisfy your needs"
        else:
            command = tables[command_id]
        success = False
        tries = 0
        while tries <= 3:
            host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = host.connect_ex((self.ip, int(self.port)))
            host.close()
            if result == 0:
                while not success:
                        try:
                            query = '[ "INSERT INTO ' + command
                            if command_id == 0:
                                query += "(ename, DateOfCreation) VALUES(\\\"" + election_name + "\\\", CURRENT_DATE)\""
                            else:
                                for i in range(0, len(candidate_list)):
                                    print(i + 1, ". ", candidate_list[i], sep = "")
                                    query += '(\\ \"' + candidate_list[i] + '\\ \",' + election_id +  ',' + str(i + 1) + '), '
                            query += " ]"
                            election_data = '[ "INSERT INTO ElectionName(ename, DateOfCreation) VALUES(\\"' + election_name +'\\", CURRENT_DATE)" ]'
                            response = requests.post(url = self.url_post, headers = self.headers, data = query)
                            return response.json()

                        except KeyboardInterrupt:
                            raise
                        except:
                            pass
            else:
                print("Port 4001 down")
                tries += 1
                if tries == 4:
                    print("Contact EVM Manager")
                    print("Exiting")
                    print("ERROR_CODE: 2", command[0], "\n", sep = '')
                    return '2' + command[0]
                print("Server not running.")
                print("Waiting for 5s\n")
                time.sleep(5)

