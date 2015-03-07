from ..dbscript import *
from sqlalchemy import Column, Integer, String, ForeignKey, Sequence, Table
from sqlalchemy.types import Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association_group_permission = Table('association_group_permission', Base.metadata,\
        Column('group_id', Integer, ForeignKey('acl_group.id')),\
        Column('permission_id', Integer, ForeignKey('acl_permission.id')))

association_permission_resource = Table('association_permission_resource', Base.metadata,\
        Column('resource_id', Integer, ForeignKey('acl_resource.id')),\
        Column('permission_id', Integer, ForeignKey('acl_permission.id')))

class Group(Base):
    __tablename__ = 'acl_group'
    id = Column(Integer, Sequence('acl_group_id'), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    remark = Column(String(255))
    permissions = relationship('Permission', secondary=association_group_permission, backref='groups') 
    def __repr__(self):
        return "<Group(id=%d, name=%s)>" % (self.id, self.name)

class User(Base):
    __tablename__ = 'acl_user'
    id = Column(Integer, Sequence('acl_user_id'), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    group_id = Column(Integer, ForeignKey('acl_group.id'))
    group = relationship('Group', backref='users')
    remark = Column(String(255))
    def __repr__(self):
        return "<User(id=%d, name=%s)>" % (self.id, self.name)

class Permission(Base):
    __tablename__ = 'acl_permission'
    id = Column(Integer, Sequence('acl_permission_id'), primary_key=True)
    name = Column(String, nullable=False, unique=True)
    allow = Column(Boolean)
    resources = relationship('Resource', secondary=association_permission_resource, backref='permissions')
    remark = Column(String(255))
    def __repr__(self):
        return "<Permission(id=%d, name=%s)>" % (self.id, self.name)

class Resource(Base):
    __tablename__ = 'acl_resource'
    id = Column(Integer, Sequence('acl_resource_id'), primary_key=True)
    path = Column(String, nullable=False)

def init_db():
    Base.metadata.drop_all(session_engine)
    Base.metadata.create_all(session_engine)

def init_data():
    session = Session()
    admin_resource = Resource(path='/admin')
    guest_select_permission = Permission(name='guest:select', allow=False, remark='reject guest view /admin') 
    guest_select_permission.resources.append(admin_resource)
    guest = Group(name='guest', remark='normal guest view on website')
    guest.permissions.append(guest_select_permission)
    session.add(guest)
    session.commit()
    session.close()

if __name__ == "__main__":
    init_db()
    init_data()
