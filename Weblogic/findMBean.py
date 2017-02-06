def findMBean(prefix, name):
  mydirs = ls(returnMap='true');

  found = [];

  pattern = java.util.regex.Pattern.compile(str(escape(prefix)) + str('.*name=') + str(escape(name)) + str('.*$'));

  for mydir in mydirs:
    x = java.lang.String(mydir);
    matcher = pattern.matcher(x);
    while matcher.find():
      found.append(x);

  return found;
