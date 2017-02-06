Criar DS

dsname="JDBCDataSource"
jdbcSR = create(dsname,"JDBCSystemResource")
theJDBCResource = jdbcSR.getJDBCResource()
theJDBCResource.setName(dsname)
connectionPoolParams = theJDBCResource.getJDBCConnectionPoolParams()
connectionPoolParams.setConnectionReserveTimeoutSeconds(25)
connectionPoolParams.setMaxCapacity(100)
connectionPoolParams.setTestTableName("SQL BEGIN NULL;END;")
dsParams = theJDBCResource.getJDBCDataSourceParams()
dsParams.addJNDIName('ds.'+dsname)
driverParams = theJDBCResource.getJDBCDriverParams()
driverParams.setUrl("STRING")
driverParams.setDriverName("DRIVER")
#driverParams.setUrl("jdbc:oracle:thin:@my-oracle-server:my-oracle-server-port:my-oracle-sid")
#driverParams.setDriverName("oracle.jdbc.driver.OracleDriver")
driverParams.setPassword("pass")
#driverParams.setLoginDelaySeconds(60)
driverProperties = driverParams.getProperties()
proper = driverProperties.createProperty("user")
#proper.setName("user")
proper.setValue("user")
proper1 = driverProperties.createProperty("DatabaseName")
#proper1.setName("DBName")
proper1.setValue("jdbc:oracle:thin://server/DB")

Ajustar parametros

cd('/JDBCSystemResources/'+x.getName()+'/Resource/'+x.getName()+'/JDBCDriverParams/'+x.getName())
    driver=cmo.getDriverName()

    if driver.count('oracle') == 1:
        cd('/JDBCSystemResources/'+x.getName()+'/Resource/'+x.getName()+'/JDBCConnectionPoolParams/'+x.getName())
        set('InactiveConnectionTimeoutSeconds','60')
        set('StatementTimeout','120')
        set('TestConnectionsOnReserve','true')
        set('MaxCapacity','20')
        set('CapacityIncrement','1')
        set('InitialCapacity','5')
        set('TestTableName','SQL BEGIN NULL; END;')
