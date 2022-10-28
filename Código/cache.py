import time

cache = {}

def start_cache(file, params):
    global cache
    try:
        with open(file) as registered_cache:
            line = registered_cache.readline()
            while line != '':
                index = line.index("=")
                request = line[0:index]
                response = line[index + 1:]
                tuple_date_response = tuple(map(str, response.split("|")))
                auxiliar = list(tuple_date_response)
                auxiliar[0] = float(auxiliar[0])
                auxiliar[1] = eval(auxiliar[1])
                tuple_date_response = tuple(auxiliar)
                cache[request] = tuple_date_response
                line = registered_cache.readline()
            check_registers_cache(file, params)
        return cache
    except:
        return cache

def deleteLines(file, linesDel):
        lines = []
        number = 0
        try:
            with open(file, 'r') as fp:
                line = fp.readline()
                lines.append(line)
                while line != "":
                    line = fp.readline()
                    lines.append(line)
            with open(file, "w") as f:
                for line in lines:
                    if not number in linesDel:
                        f.write(line)
                    number += 1
        except:
            return

def check_registers_cache(file, params):
    global cache
    linesToDelete = []
    number = 0
    try:
        with open(file) as registered_cache:
            line = registered_cache.readline()
            while line != "":
                index = line.index("=")
                request = line[:index]
                response = line[index + 1:]
                tuple_date_response = tuple(map(str, response.split("|")))
                auxiliar = list(tuple_date_response)
                if (time.time() - float(auxiliar[0])) / 60 >= params['ttl']:
                    linesToDelete.append(number)
                    cache.pop(request)
                number += 1
                line = registered_cache.readline()
            deleteLines(file, linesToDelete)
        return cache
    except:
        return

def add_cache(request, response, params):
    try:
        with open("cache.txt", "a") as f:
            f.write(f'{request}={time.time()}|{response}\n')
        cache[request] = tuple([time.time(), response])
        check_registers_cache("cache.txt", params)
    except:
        return
