#!/bin/bash
# 说明：安装mysql-8.0.27
# 日期：2022-01-12
set -ex

yum update perl* -y
yum install perl-JSON.noarch perl-JSON-PP.noarch  perl-JSON-tests.noarch wget libaio* unzip lrzsz net-tools vim git tree zip -y

wget https://downloads.percona.com/downloads/Percona-XtraDB-Cluster-LATEST/Percona-XtraDB-Cluster-8.0.25/binary/redhat/7/x86_64/percona-xtradb-cluster-shared-8.0.25-15.1.el7.x86_64.rpm
yum remove -y mariadb-libs
rpm -ivh percona-xtradb-cluster-shared-8.0.25-15.1.el7.x86_64.rpm

wget https://repo.mysql.com//mysql80-community-release-el7-1.noarch.rpm
rpm -ivh mysql80-community-release-el7-1.noarch.rpm

# yum install mysql-community-server -y    # 默认是安装最新的版本
yum install mysql-community-server-8.0.27-1.el7 -y
systemctl start mysqld
systemctl enable mysqld
systemctl is-active mysqld
