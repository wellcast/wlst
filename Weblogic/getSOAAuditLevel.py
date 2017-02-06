redirect('/dev/null', 'false')
connect('weblogic','pass','t3://local:21210')
f = open('/tmp/checkSOAAuditLevel.txt', 'w')
custom()
cd('oracle.soa.config')
clist = ls(returnMap='true')
for c in clist:
     #print "item: " + str(c)
     try:
          o = ObjectName(str(c))
          if str(o.getKeyProperty('j2eeType')) == 'SCAComposite':
               props = mbs.getAttribute(o, 'Properties')
               try:
                    level = str(props[0].get('value'))
               except:
                    level = 'Inherit'

               try:
                    name = mbs.getAttribute(o, 'Name')
               except:
                    name = str(c)
               if level != 'Off' and level != 'Inherit':
                    print >>f, "composite:'"+name+"', level:'"+level+"'"
     except:
          continue;
f.close()
disconnect()
exit()
