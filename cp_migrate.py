#!/usr/bin/python

import requests
import base64
import json
import os
import argparse
import yaml

## retrieve key and secret from vault
vault_key=str(os.popen('sudo cat /home/t/etc/vault_key').read())

curl_key_string="curl -sX GET -u " + vault_key + " https://vault.com/values/catchpoint_api_key/key"
client_key=os.popen(curl_key_string).read()

curl_secret_string="curl -sX GET -u " + vault_key + " https://vault.com/values/catchpoint_api_secret/secret"
client_secret=os.popen(curl_secret_string).read()


## build api endpoint
uri="https://io.catchpoint.com/ui/api/"
version="v1"

## just need user to provide testid(s) on cmd line
parser = argparse.ArgumentParser(description='retrieve test_id from user input')
parser.add_argument('-t', '--testid', type=str, help='id for test in catchpoint')
parser.add_argument('-d', '--divid', type=str, help='"client" = client division, "nonprod" = non-prod division, "dev" = dev division')
                    
args = parser.parse_args()

def token_():
    ### Uses key and secret created through UI for oauth2 framework to
    ### generate an access token
    token_uri = uri + "token" 
    client_auth = requests.auth.HTTPBasicAuth(client_key, client_secret)
    post_data = {"grant_type": "client_credentials"}
    response = requests.post(token_uri, auth=client_auth, data=post_data)
    token = response.json()
    enc = base64.b64encode(token['access_token'])
    return enc

def get_tests(testid):
    ### returns test properties, provides name, url, status, etc.
    end_point = uri + version + "/" + "tests/" + testid 
    headers = {"Authorization": "bearer %s" % token_()}
    try:
        response = requests.get(end_point, headers=headers)
        return response.json()
    except Exception as e:
        return e

def new_test(payload):
    ### generates a new test. test configs pulled from get_tests() 
    end_point = uri + version + "/" + "tests/" + "0"
    headers = {"Authorization": "bearer %s" % token_()}
    try:
        newpost = requests.post(end_point, headers=headers, data=payload)
        if newpost.status_code == 200:
            print "Test successfully created." 
            print "\n"
            print "Navigate to %s Division, Staging Product to find new test" % args.divid
        else:
            print newpost.raise_for_status()
    except Exception as e:
         print e  
         print "Error: Check test configuration, the API only likes inherited settings"

def instant_tests(testid):
    ### work in progress, not yet working
    ### would like to have an option to run this when a new test is created
    end_point = uri + version + "/" + "InstantTest/" + "0" 
    headers = {"Authorization": "bearer %s" % token_()}
    try:
        response = requests.get(end_point, headers=headers)
        print response.json()
    except Exception as e:
        return e   

def del_pf():
    del test_prop['parent_folder_id']

def dst_div(div_):
    f = open('conf.yml')
    conf = yaml.load(f)
    div_id = conf['div_']
    if div_ == "adplatform":
        pr_id = conf['z-stage_product']
        test_prop['division_id'] = div_id
        test_prop['product_id'] = pr_id
        test_prop['id'] = 0
        if 'parent_folder_id' in test_prop:
            del_pf()
            json_text = json.dumps(test_prop)
            new_test(json_text)
        else:
            json_text = json.dumps(test_prop)
            new_test(json_text)
    elif div_ == "client":
        pr_id = conf['staging_product']
        test_prop['division_id'] = div_id
        test_prop['product_id'] = pr_id
        test_prop['id'] = 0
        if 'parent_folder_id' in test_prop:
            del_pf()
            json_text = json.dumps(test_prop)
            new_test(json_text)
        else:
            json_text = json.dumps(test_prop)
            new_test(json_text)

def dev_division():
    f = open('conf.yml')
    conf = yaml.load(f)
    div_id = conf['dev_div']
    pr_id = conf['z-stage_product']
    test_prop['division_id'] = div_id
    test_prop['product_id'] = pr_id
    test_prop['id'] = 0
    if 'parent_folder_id' in test_prop:
        del_pf()
        json_text = json.dumps(test_prop)
        new_test(json_text)
    else:
        json_text = json.dumps(test_prop)
        new_test(json_text)

def client_div():
    f = open('conf.yml')
    conf = yaml.load(f)
    div_id = conf['client_div']
    pr_id = conf['staging_product']
    test_prop['division_id'] = div_id
    test_prop['product_id'] = pr_id
    test_prop['id'] = 0
    if 'parent_folder_id' in test_prop:
        del_pf()
        json_text = json.dumps(test_prop)
        new_test(json_text)
    else:
        json_text = json.dumps(test_prop)
        new_test(json_text)

if __name__ == '__main__':
    test_prop = get_tests(args.testid)
    print "migrating the test: " + test_prop['name'] + " " + "url: " + test_prop['test_url']
    print "\n"
    if args.divid == "adplatform":
        adp_pltfrm()
    elif args.divid == "client":
        client_div() 

    """
    ### run instant test
    json_text = json.dumps(test_prop)
    print json_text 
    instant_tests(args.testid)
    """
