#!/usr/bin/python
import ConfigParser
configFile = "/tmp/docker.cfg"


def configLoad(configfile):
  config = ConfigParser.SafeConfigParser()
  config.read(configfile);
  results=[]
  for i in config.sections():
    ans={};
    if "name" in config.options(i):
      ans["name"] = config.get(i,"name");
    else:
      print("Key Name not found in section.")
      raise KeyError
    if "url" in config.options(i):
      ans["url"] = config.get(i,"url");
    else:
      print("Key Url not found in section.")
      raise KeyError
    if "version" in config.options(i):
      ans["version"] = config.get(i,"version");
    else:
      ans["version"] = "1.26";
    if "role" in config.options(i):
      ans["role"] = config.get(i,"role");
    results.append(ans);
  return results

