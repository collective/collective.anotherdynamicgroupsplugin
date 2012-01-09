from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

def add_user(user_id, roles=None):    
    portal = getSite()
    user_folder = getToolByName(portal, 'acl_users')
    
    if roles is None:
        roles = ['Member']
    
    user_folder.userFolderAddUser(user_id, user_id, roles, None)
    return user_folder.getUser(user_id)
