import json


class Dictionary:
    def parseInfo(self, httpReq):
        data = httpReq.split("\r\n")
        requestType = data[0].split(" ")

        requestDictionary = {
            'Method': requestType[0],
            'Url': requestType[1],
            'Version': requestType[2]
        }

        params = {}

        for x in range(1, len(data)):
            separated = data[x].split(":")
            if len(separated) == 2:
                requestDictionary.update({separated[0]: separated[1]})

        if len(requestDictionary['Url']) > 1:
            if requestDictionary['Method'] == 'GET':
                if '?' in requestDictionary['Url']:
                    get = requestDictionary['Url'].split("?")
                    if '%22' in get[1]:
                        get[1] = get[1].replace('%22', '')

                    if '%20' in get[1]:
                        get[1] = get[1].replace('%20', ' ')

                    if '&' in get[1]:
                        petition = get[1].split("&")
                        for p in petition:
                            param = p.split("=")
                            params.update({param[0]: param[1]})
                    else:
                        petition = get[1]
                        param = petition.split("=")
                        params.update({param[0]: param[1]})

            elif requestDictionary['Method'] == 'POST':
                completereq = data[len(data) - 1]

                if '&' in completereq:
                    petition = completereq.split("&")
                    for p in petition:
                        param = p.split("=")
                        params.update({param[0]: param[1]})
                else:
                    petition = completereq
                    param = petition.split("=")
                    params.update({param[0]: param[1]})

        requestDictionary.update({'params': params})
        return requestDictionary
