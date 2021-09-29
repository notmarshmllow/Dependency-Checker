#Dependency Checker v1
#Tool to find dependency confusion issues in entire GitHub organization and individual repositories.
#More info: https://github.com/notmarshmllow/Dependency-Checker
#Coded by @notmarshmllow (https://notmarshmllow.github.io/blog)

from __future__ import print_function
from os import execl, replace
import cred
import argparse
import requests
from bs4 import BeautifulSoup
import codecs
from termcolor import colored
from colorama import init
import importlib
from urlextract import  URLExtract
import threading
import sys
import os.path
import json
import pandas as pd




init()

parser = argparse.ArgumentParser(description="Dependency Checker. Find misconfigured Dependencies. Coded by @notmarshmllow")
parser.add_argument('-u', help='URL of Repository.', type=str, required=False)
parser.add_argument('-org', help='Org Name.', type=str)
parser.add_argument('-p', help='Page Number.', type=int)
parser.add_argument('-o', help='Wite output to a file.', type=str)
parser.add_argument('-v', help='Verbose Mode.', action="count")
parser.add_argument('-s', help='Silent Mode. No Output.', action="count")
args = parser.parse_args()

def banner():
    print('''
██████╗ ███████╗██████╗ ███████╗███╗   ██╗██████╗ ███████╗███╗   ██╗ ██████╗██╗   ██╗    
██╔══██╗██╔════╝██╔══██╗██╔════╝████╗  ██║██╔══██╗██╔════╝████╗  ██║██╔════╝╚██╗ ██╔╝    
██║  ██║█████╗  ██████╔╝█████╗  ██╔██╗ ██║██║  ██║█████╗  ██╔██╗ ██║██║      ╚████╔╝     
██║  ██║██╔══╝  ██╔═══╝ ██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██║╚██╗██║██║       ╚██╔╝      
██████╔╝███████╗██║     ███████╗██║ ╚████║██████╔╝███████╗██║ ╚████║╚██████╗   ██║       
╚═════╝ ╚══════╝╚═╝     ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═══╝ ╚═════╝   ╚═╝       
                                                                                         
 ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗                                  
██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗                                 
██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝                                 
██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗                                 
╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║                                 
 ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝  
                               > Created by @notmarshmllow
                    > https://notmarshmllow.github.io/blog
    
------------------------------------------------------------------------------------
    ''')
if not args.s:
    banner()

if args.p:
    page_to_scan = args.p
else:
    args.p = 100
    args.p = (args.p)

def scan_info():
    if args.org:
        print(f'Organization: {str(args.org)}')
        print(f'Pages: {str(args.p)}')
        print('\n')

scan_info()


if args.o:
    try:
        if os.path.isfile(args.o):
                print('Output file already exists. Overwriting file.\n\n ')
                os.remove(args.o)
                output_file = open(args.o, 'a')
    except FileNotFoundError:
        print('Invalid Path or filename.\n\nExiting...')
        sys.exit(1)
    else:
        try:
            output_file = open(args.o, 'a')
        except FileNotFoundError:
            print('Invalid Path or filename.\n\nExiting...')
            sys.exit(1)

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'
}

login_data = cred.credentials

try:
    with requests.Session() as s:
        url = 'https://github.com/session'
        r = s.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        login_data['timestamp_secret'] = soup.find('input', attrs={'name':'timestamp_secret'})['value']
        login_data['timestamp'] = soup.find('input', attrs={'name':'timestamp'})['value']
        login_data['authenticity_token'] = soup.find('input', attrs={'name':'authenticity_token'})['value']

        r = s.post(url, data=login_data, headers=headers)
except:
    print('Login Error.')



input_url = str(args.u)
if input_url[-3:] == '.go':
    print(colored('Please provide URL of the repository where the GO file exists and not URL of the file directly.\n', "red"))
    sys.exit(1)
elif input_url[-3:] == '.js':
        print(colored('Please provide URL of the repository where the JSON file exists and not URL of the file directly.\n', "red"))
        sys.exit(1)
elif input_url[-3:] == '.py':
    print(colored('Please provide URL of the repository where the Python file exists and not URL of the file directly.\n', "red"))
    sys.exit(1)


py = []
go = []
json = []
postscanodt = []


if args.org:

    
    
    organization = str(args.org)
    organization_slashed = '/'+organization+'/'
    query_py = "filename:.py"
    query_json = 'filename:.json'
    query_go = 'filename:.go'

    
    def py_fch_org():

        
        x = 1

        while x <=(args.p):
            #url_org_py = f'https://github.com/search?p={x}&q=org%3A{organization}+{query_py}&type=code'
            url_org_py = f'https://github.com/search?l=Python&p={x}&q=org%3A{organization}&type=Code'

            py_page = s.get(url_org_py).text
            if 'We couldnt find any code matching' in py_page:
                print(colored('\nNo Repositories Found. Please check the Organization name.' , 'red'))
                sys.exit(1)
            soup_py = BeautifulSoup(py_page, 'html5lib')

            for link in soup_py.findAll('a'):
                inside_file_py = link.get('href')
                full_url_py = 'https://github.com/' + inside_file_py
                if full_url_py[-3:] == '.py' and organization_slashed in full_url_py:
                    if full_url_py not in py:
                        py.append(full_url_py)

            x+=1

    def json_fch_org():

        x = (args.p)

        while x <= (args.p):
            #url_org_json = f'https://github.com/search?p={x}&q=org%3A{organization}+{query_json}&type=code'
            url_org_json = f'https://github.com/search?l=JSON&p={x}&q=org%3A{organization}&type=Code'


            json_page = s.get(url_org_json).text
            if 'We couldnt find any code matching' in json_page:
                print(colored('\nNo Repositories Found. Please check the Organization name.' , 'red'))
                sys.exit(1)
            soup_json = BeautifulSoup(json_page, 'html5lib')

            for link in soup_json.findAll('a'):
                inside_file_json = link.get('href')
                full_url_json = 'https://github.com/' + inside_file_json
                if full_url_json[-5:] == '.json' and organization_slashed in full_url_json:
                    if full_url_json not in json:
                        json.append(full_url_json)

            x+=1

    def go_fch_org():

        x= (args.p)

        while x <= (args.p):
            #url_org_go = f'https://github.com/search?p={x}&q=org%3A{organization}+{query_go}&type=code'
            url_org_go = f'https://github.com/search?l=Go&p={x}&q=org%3A{organization}&type=Code'


            go_page = s.get(url_org_go).text
            if 'We couldnt find any code matching' in go_page:
                print(colored('\nNo Repositories Found. Please check the Organization name.' , 'red'))
                sys.exit(1)
            soup_go = BeautifulSoup(go_page, 'html5lib')

            for link in soup_go.findAll('a'):
                inside_file_go = link.get('href')
                full_url_go = 'https://github.com/' + inside_file_go
                if full_url_go[-3:] == '.go' and organization_slashed in full_url_go:
                    if full_url_go not in go:
                        go.append(full_url_go)

            x+=1

if args.u:
    input_url = input_url.split('/')
    input_org = input_url[3]

    def urls():
        oragnization_name = input_org

        org_url = str(args.u)
        try:
            org_html = requests.get(org_url)
        except:
            print('Error while fetching repository.')
        soup0 = BeautifulSoup(org_html.text, 'html.parser')
        for link in soup0.findAll('a'):
            repo_url = 'https://github.com/'+link.get('href') #all urls in root level

            if oragnization_name in repo_url:
                if '.py' in repo_url:
                    py.append(repo_url)
                if '.go' in repo_url:
                    go.append(repo_url)
                if '.json' in repo_url:
                    json.append(repo_url)      


#-------------------------------------------------------------


donescan = []

def pyt():
    if len(py) > 0:
        if not args.s: 
            print(colored('\n-----------------------------------', 'green'))
            print(colored('> Checking for Python Dependencies', 'green'))
            print(colored('-----------------------------------\n', 'green'))
        for i in py:
            i = i.replace('https://github.com/', 'https://raw.githubusercontent.com/').replace('blob/', '')
            repo_data = requests.get(i, stream=True)
            for line in repo_data.iter_lines():
                if line: 
                    line = codecs.decode(line, 'UTF-8')
                    if line.startswith('import'):
                        breakup = line.split()
                        breakup[::2]
                        libs = str(breakup[1]).replace(')', '').replace('(', '').replace(']', '').replace('[', '')
                        
                        try:
                            head, sep, tail = libs.partition('.')
                            libs = head 
                        except:
                            continue
                        if libs not in donescan: 
                            vuln_py_lib = requests.get('https://pypi.org/project/'+(libs))
                            if vuln_py_lib.status_code == 404:
                                try:
                                    spam_loader = importlib.util.find_spec(libs)
                                    found = spam_loader is not None
                                    if found == False:
                                        if not args.s:  
                                            print(colored(f'[Python Package : {libs}] - ', 'red') + i)
                                            if args.o:
                                                msg_py = ((f'[Python Package : {libs}] -> ') + i)
                                                output_file.write(msg_py+'\n')                                    
                                    

                                except:
                                    if not args.s:
                                        print(colored(f'[Python Package : {libs}] - ', 'red') + i)
                                        if args.o:
                                            msg_py = ((f'[Python Package : {libs}] -> ') + i)
                                            output_file.write(msg_py+'\n')                                    
                            if vuln_py_lib.status_code == 200:
                                if args.v:
                                    if not args.s:
                                        print(libs + ' - ' + colored("Python Package Exist", "green"))
                                    if args.v and args.o:
                                        msg_py = (str(libs) + ' - ' + ("Python Package Exist"))
                                        output_file.write(msg_py+'\n')

                            donescan.append(libs)
                                            

                    elif line.startswith('from'):
                        breakup = line.split()
                        breakup[::2]
                        libs = str(breakup[1]).replace(',', '').replace('[', '').replace(']', '')

                        if ')' in libs:
                            break
                        elif '(' in libs:
                            break
                        elif '_' in libs:
                            break
                        elif libs in postscanodt:
                            break
                        elif libs in donescan:
                            break

                        else:
                            try:
                                head, sep, tail = libs.partition('.')
                                libs = head 
                            except:
                                continue
                            if str(libs) not in donescan:
                                vuln_py_lib = requests.get('https://pypi.org/project/'+str(libs).replace(',', '').replace('__', '').replace(']', '').replace('[', ''))
                                if vuln_py_lib.status_code == 404:
                                    if not args.s:
                                        print(colored(f'[Python Package : {libs}] - ', 'red') + i)
                                        if args.o:
                                            msg_py = ((f'[Python Package : {libs}] -> ') +  i)
                                            output_file.write(msg_py+'\n')   
                                    
                                if vuln_py_lib.status_code == 200:
                                    if args.v:
                                        if not args.s:
                                            print(libs + ' - ' + colored("Python Package Exist", "green"))
                                        if args.v and args.o:
                                            msg_py = (str(libs) + ' - ' + ("Python Package Exist"))
                                            output_file.write(msg_py+'\n')
                                    
                                donescan.append(libs)
                                



#--------------------------------------------------------------------

    if len(json) > 0:
        if not args.s:
            print(colored('\n--------------------------------', 'green'))
            print(colored('> Checking for NPM Dependencies', 'green'))
            print(colored('--------------------------------\n', 'green'))
        for j in json:
            j = j.replace('https://github.com/', 'https://raw.githubusercontent.com/').replace('blob/', '')


            repo_data = requests.get(j)
            repo_data_json = (repo_data.json())
            
            depedency_list = []
            
            def requires(d):
                for kx, v in d.items():
                    if kx == 'requires':
                        if isinstance(v, dict):
                            for _kx, _v in v.items():
                                depedency_list.append(_kx)
                                
                        else:
                            pass
                    else:
                        if isinstance(v, dict):
                            requires(v)
                    


            requires(repo_data_json)



            
            try:
                dependencies1 = repo_data_json["devDependencies"]
                for key in dependencies1.keys():
                    if isinstance(dependencies1[key], dict) == False:
                        depedency_list.append(key)
            except:
                pass

            try:
                dependencies2 = repo_data_json["dependencies"]
                for key in dependencies2.keys():
                    if isinstance(dependencies2[key], dict) == False:
                        depedency_list.append(key)
            except:
                pass

            try:
                for key in str(repo_data_json).replace("'", "").replace("{", "").replace("}", "").replace(":", "").replace(',', '').split():
                    if key.startswith('@'):
                        depedency_list.append(key)
            except:
                pass
            

            dependencies_list = list(set(depedency_list))


            for word in dependencies_list:
                check_dependency = requests.get('https://www.npmjs.com/package/'+word)
                if check_dependency.status_code == 404:
                    if not args.s:
                        print(colored(f'[!] Vulnerable Repository [NPM Package : {word}] -> ', 'red') + j)
                        
                    if args.o:
                        msg_npm = ((f'[!] Vulnerable Repository [NPM Package : {word}] -> ') +  j)
                        output_file.write(msg_npm + '\n')
                else:
                    if args.v:
                        if not args.s:
                            print(word + ' - ' + colored("NPM Package Exist.", "green"))
                        
                    if args.v and args.o:
                        msg_npm=(word + ' - ' + ("NPM Package Exist."))
                        output_file.write(msg_npm + '\n')


#-----------------------------------------------------

    if len(go) > 0:
        if not args.s:
            print(colored('\n-------------------------------', 'green'))
            print(colored('> Checking for GO Dependencies', 'green'))
            print(colored('-------------------------------\n', 'green'))
        imported_dependencies = []
        dependency_urls = []
        nc_urls = []

        for k in go:
            k = k.replace('https://github.com/', 'https://raw.githubusercontent.com/').replace('blob/', '')
            nc_urls.append(k)
    
        nc_urls = list(set(nc_urls))

        extractor = URLExtract()

        for nc_fetch in nc_urls:
            repo_data_go = requests.get(nc_fetch, stream=True)

            for line in repo_data_go.iter_lines():
                if line: 
                    line = codecs.decode(line, 'UTF-8').strip()
                    if line.startswith('"'):
                        if line not in imported_dependencies:
                            if 'github.com' not in line:
                                imported_dependencies.append(str(line))
                        
                    for go_url in extractor.gen_urls(str(line)):
                        if 'github.com' in go_url:
                            modify_go_url = str(go_url).replace('"', '').split('/')
                            modify_go_url = modify_go_url[0] + '/' + modify_go_url[1]
                            if modify_go_url not in dependency_urls:
                                dependency_urls.append(modify_go_url)

        for i in imported_dependencies:
            i = str(i).replace('"', '')
            try:
                resi = requests.get('https://pkg.go.dev/'+i)
                if resi.status_code == 404:
                        if not args.s:
                            print(i + ' - ' + colored("This Go package doesn't exist.", "red"))
                        if args.o:
                            msg_go = (i + ' - ' + ("This Go package doesn't exist."))
                            output_file.write(msg_go+'\n')

                if resi.status_code == 200:
                    if not args.s:
                        print(colored(i + ' - ' + colored("Go package exist.", "green")))
                    if args.v and args.o:
                        (i + ' - ' + ("Go package exist."))
                        output_file.write(msg_go+'\n')

            except:
                pass
        
        for j in dependency_urls:
            url_new = 'https://' + j
            try:
                resj = requests.get(url_new)
                if resj.status_code == 404:
                    if not args.s:
                        print(url_new + ' - ' + colored("This Go Package doesn't exist.", "red"))  
                    if args.v and args.o:
                        msg_go  = (url_new + ' - ' + ("This Go Package doesn't exist."))
                        output_file.write(msg_go+'\n')
                elif resj.status_code == 200:
                    if not args.s:
                        print(url_new + ' - ' + colored("Go Package exist.", "green"))
                        print(msg_go)
                    if args.v and args.o:
                        msg_go = (url_new + ' - ' + ("Go Package exist."))
                        output_file.write(msg_go+'\n')
                    
            except:
                pass



threads = []


if args.u:
    t = threading.Thread(target=urls)
    t.start()
    threads.append(t)
    for thread in threads:
        thread.join()

if args.org:
    
    try: 
        t1 = threading.Thread(target=py_fch_org, daemon=True)
        t1.start()
        while t1.is_alive():
            t1.join(1)
    except KeyboardInterrupt:
        print('\n\nExiting ... ')
        sys.exit(1)

    try: 
        t2 = threading.Thread(target=json_fch_org, daemon=True)
        t2.start()
        while t2.is_alive():
            t2.join(1)
    except KeyboardInterrupt:
        print('\n\nExiting ... ')
        sys.exit(1)

    try: 
        t3 = threading.Thread(target=go_fch_org, daemon=True)
        t3.start()
        while t3.is_alive():
            t3.join(1)
    except KeyboardInterrupt:
        print('\n\nExiting ... ')
        sys.exit(1)

try: 
    t = threading.Thread(target=pyt, daemon=True)
    t.start()
    while t.is_alive():
        t.join(1)
except KeyboardInterrupt:
    print('\n\nExiting ... ')
    sys.exit(1)

