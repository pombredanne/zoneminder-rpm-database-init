# -*- coding: utf-8 -*- 

import ConfigParser
import os.path

class Configuration:
  """ Configuration reader and writer for zm_database_init script """
  
  # static members
  MySection = "ZmDatabaseInit"
  ZmSection = "ZoneMinder"
  
  def __init__(self, filename):
    self.filename = filename
    self.config = ConfigParser.SafeConfigParser()
    self.configModified = False
    
    self.readConfiguration()
  
  def __enter__(self):
    return self
  
  def readConfiguration(self):
    if os.path.isfile(self.filename):
      self.config.read(self.filename)
  
  def _readSetting(self, section, optionName, defaultValue, getFunction=None):
    if not getFunction:
      getFunction = self.config.get
      
    if not self.config.has_section(section):
      self.config.add_section(section)
      self.configModified = True
    
    if not self.config.has_option(section, optionName):
      self.config.set(section, optionName, defaultValue)
      self.configModified = True
    
    return getFunction(section, optionName)
  
  def zmLockFile(self):
    return self._readSetting(Configuration.ZmSection, "lock-file", "/usr/share/zm/lock")
  
  def zmPath(self):
    return self._readSetting(Configuration.ZmSection, "data-install-path", "/usr/share/zm")
  
  def zmConfigFile(self):
    return self._readSetting(Configuration.ZmSection, "configuration-file", "/etc/zm.conf")
  
  def installedZmVersionFile(self):
    return self._readSetting(Configuration.ZmSection, "version-file", "/usr/share/zm/version")
  
  def createDatabaseSqlFile(self):
    return self._readSetting(Configuration.ZmSection, "create-database-sql-file", "/usr/share/zm/db/zm_create.sql")
  
  def zmUpdateScriptPath(self):
    return self._readSetting(Configuration.ZmSection, "path-to-zmupdate", "/usr/bin/zmupdate.pl")
  
  def zmUpdateBackupDatabase(self):
    return self._readSetting(Configuration.ZmSection, "backup-database-during-zmudpate", "yes", self.config.getboolean)
  
  def databaseInitialized(self):
    return self._readSetting(Configuration.MySection, "database-initialized", "no", self.config.getboolean)
  
  def setDatabaseInitialized(self, initialized):
    value = "no"
    if initialized:
      value = "yes"
    self.config.set(Configuration.MySection, "database-initialized", value)
    self.configModified = True
  
  def rootUserCheck(self):
    return self._readSetting(Configuration.MySection, "allow-execution-only-as-root", "yes", self.config.getboolean)
  
  def mysqlHost(self):
    return self._readSetting(Configuration.MySection, "mysql-host", "localhost")
  
  def setMysqlHost(self, hostname):
    if self.mysqlHost() == hostname:
      return
    
    self.config.set(MySection, "mysql-host", hostname)
    self.configModified = True
  
  def mysqlBin(self):
    return self._readSetting(Configuration.MySection, "mysql-bin", "/usr/bin/mysql")
  
  def checkConfigUpdate(self):
    if self.configModified:
      with open(self.filename, "w") as f:
        self.config.write(f)
      
      self.configModified = False
  
  def __exit__(self, type, value, traceback):
    self.checkConfigUpdate()
  
  def __del__(self):
    self.checkConfigUpdate()
    
    
