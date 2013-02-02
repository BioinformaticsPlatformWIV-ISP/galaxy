from tool_shed.base.twilltestcase import ShedTwillTestCase, common, os
import tool_shed.base.test_db_util as test_db_util

datatypes_repository_name = 'emboss_datatypes_0030'
datatypes_repository_description = "Galaxy applicable data formats used by Emboss tools."
datatypes_repository_long_description = "Galaxy applicable data formats used by Emboss tools.  This repository contains no tools."

emboss_repository_name = 'emboss_0030'
emboss_5_repository_name = 'emboss_5_0030'
emboss_6_repository_name = 'emboss_6_0030'
emboss_repository_description = 'Galaxy wrappers for Emboss version 5.0.0 tools'
emboss_repository_long_description = 'Galaxy wrappers for Emboss version 5.0.0 tools'

base_datatypes_count = 0
repository_datatypes_count = 0
running_standalone = False

class RepositoryWithDependencyRevisions( ShedTwillTestCase ):
    '''Test installing a repository with dependency revisions.'''
    def test_0000_initiate_users( self ):
        """Create necessary user accounts."""
        self.logout()
        self.login( email=common.test_user_1_email, username=common.test_user_1_name )
        test_user_1 = test_db_util.get_user( common.test_user_1_email )
        assert test_user_1 is not None, 'Problem retrieving user with email %s from the database' % test_user_1_email
        test_user_1_private_role = test_db_util.get_private_role( test_user_1 )
        self.logout()
        self.login( email=common.admin_email, username=common.admin_username )
        admin_user = test_db_util.get_user( common.admin_email )
        assert admin_user is not None, 'Problem retrieving user with email %s from the database' % common.admin_email
        admin_user_private_role = test_db_util.get_private_role( admin_user )
        self.galaxy_logout()
        self.galaxy_login( email=common.admin_email, username=common.admin_username )
        galaxy_admin_user = test_db_util.get_galaxy_user( common.admin_email )
        assert galaxy_admin_user is not None, 'Problem retrieving user with email %s from the database' % common.admin_email
        galaxy_admin_user_private_role = test_db_util.get_galaxy_private_role( galaxy_admin_user )
    def test_0005_ensure_repositories_and_categories_exist( self ):
        '''Create the 0030 category and add repositories to it, if necessary.'''
        global repository_datatypes_count
        global running_standalone
        category = self.create_category( name='Test 0030 Repository Dependency Revisions', description='Test 0030 Repository Dependency Revisions' )
        self.logout()
        self.login( email=common.test_user_1_email, username=common.test_user_1_name )
        datatypes_repository = self.get_or_create_repository( name=datatypes_repository_name, 
                                                              description=datatypes_repository_description, 
                                                              long_description=datatypes_repository_long_description, 
                                                              owner=common.test_user_1_name,
                                                              category_id=self.security.encode_id( category.id ), 
                                                              strings_displayed=[] )
        if self.repository_is_new( datatypes_repository ):
            running_standalone = True
            self.upload_file( datatypes_repository, 'emboss/datatypes/datatypes_conf.xml', commit_message='Uploaded datatypes_conf.xml.' )
            emboss_5_repository = self.get_or_create_repository( name=emboss_5_repository_name, 
                                                                 description=emboss_repository_description, 
                                                                 long_description=emboss_repository_long_description, 
                                                                 owner=common.test_user_1_name,
                                                                 category_id=self.security.encode_id( category.id ), 
                                                                 strings_displayed=[] )
            self.upload_file( emboss_5_repository, 'emboss/emboss.tar', commit_message='Uploaded emboss.tar' )
            repository_dependencies_path = self.generate_temp_path( 'test_1030', additional_paths=[ 'emboss', '5' ] )
            self.generate_repository_dependency_xml( [ datatypes_repository ], 
                                                     self.get_filename( 'repository_dependencies.xml', filepath=repository_dependencies_path ) )
            self.upload_file( emboss_5_repository, 
                              'repository_dependencies.xml', 
                              filepath=repository_dependencies_path, 
                              commit_message='Uploaded repository_dependencies.xml' )
            emboss_6_repository = self.get_or_create_repository( name=emboss_6_repository_name, 
                                                                 description=emboss_repository_description, 
                                                                 long_description=emboss_repository_long_description, 
                                                                 owner=common.test_user_1_name,
                                                                 category_id=self.security.encode_id( category.id ), 
                                                                 strings_displayed=[] )
            self.upload_file( emboss_6_repository, 'emboss/emboss.tar', commit_message='Uploaded emboss.tar' )
            repository_dependencies_path = self.generate_temp_path( 'test_1030', additional_paths=[ 'emboss', '6' ] )
            self.generate_repository_dependency_xml( [ datatypes_repository ], 
                                                     self.get_filename( 'repository_dependencies.xml', filepath=repository_dependencies_path ) )
            self.upload_file( emboss_6_repository, 
                              'repository_dependencies.xml', 
                              filepath=repository_dependencies_path, 
                              commit_message='Uploaded repository_dependencies.xml' )
            emboss_repository = self.get_or_create_repository( name=emboss_repository_name, 
                                                               description=emboss_repository_description, 
                                                               long_description=emboss_repository_long_description, 
                                                               owner=common.test_user_1_name,
                                                               category_id=self.security.encode_id( category.id ), 
                                                               strings_displayed=[] )
            self.upload_file( emboss_repository, 'emboss/emboss.tar', commit_message='Uploaded emboss.tar' )
            repository_dependencies_path = self.generate_temp_path( 'test_1030', additional_paths=[ 'emboss', '5' ] )
            self.generate_repository_dependency_xml( [ emboss_5_repository ], 
                                                     self.get_filename( 'repository_dependencies.xml', filepath=repository_dependencies_path ) )
            self.upload_file( emboss_repository, 
                              'repository_dependencies.xml', 
                              filepath=repository_dependencies_path, 
                              commit_message='Uploaded repository_dependencies.xml' )
            self.generate_repository_dependency_xml( [ emboss_6_repository ], 
                                                     self.get_filename( 'repository_dependencies.xml', filepath=repository_dependencies_path ) )
            self.upload_file( emboss_repository, 
                              'repository_dependencies.xml', 
                              filepath=repository_dependencies_path, 
                              commit_message='Uploaded repository_dependencies.xml' )
        repository_datatypes_count = int( self.get_repository_datatypes_count( datatypes_repository ) )
    def test_0010_browse_tool_shed( self ):
        """Browse the available tool sheds in this Galaxy instance and preview the emboss tool."""
        self.galaxy_logout()
        self.galaxy_login( email=common.admin_email, username=common.admin_username )
        self.browse_tool_shed( url=self.url, strings_displayed=[ 'Test 0030 Repository Dependency Revisions' ] )
        category = test_db_util.get_category_by_name( 'Test 0030 Repository Dependency Revisions' )
        self.browse_category( category, strings_displayed=[ 'emboss_0030' ] )
        self.preview_repository_in_tool_shed( 'emboss_0030', common.test_user_1_name, strings_displayed=[ 'emboss_0030', 'Valid tools' ] )
    def test_0015_install_emboss_repository( self ):
        '''Install the emboss repository without installing tool dependencies.'''
        global repository_datatypes_count
        global base_datatypes_count
        global running_standalone
        base_datatypes_count = int( self.get_datatypes_count() )
        strings_displayed = [ 'Handle', 'Never installed', 'tool dependencies', 'emboss', '5.0.0', 'package' ]
        self.install_repository( 'emboss_0030', 
                                 common.test_user_1_name, 
                                 'Test 0030 Repository Dependency Revisions',
                                 strings_displayed=strings_displayed,
                                 install_tool_dependencies=False, 
                                 new_tool_panel_section='test_1030' )
        installed_repository = test_db_util.get_installed_repository_by_name_owner( 'emboss_0030', common.test_user_1_name )
        strings_displayed = [ installed_repository.name,
                              installed_repository.description,
                              installed_repository.owner, 
                              installed_repository.tool_shed, 
                              installed_repository.installed_changeset_revision ]
        self.display_galaxy_browse_repositories_page( strings_displayed=strings_displayed )
        self.display_installed_repository_manage_page( installed_repository, 
                                                       strings_displayed=[ 'Installed tool shed repository', 'Valid tools', 'antigenic' ] )
        self.check_installed_repository_tool_dependencies( installed_repository, dependencies_installed=False )
        self.verify_tool_metadata_for_installed_repository( installed_repository )
        self.update_installed_repository( installed_repository, strings_displayed=[ "there are no updates available" ] )
        current_datatypes = int( self.get_datatypes_count() )
        if running_standalone:
            assert current_datatypes == base_datatypes_count + repository_datatypes_count, 'Installing emboss did not add new datatypes.'
        else:
            assert current_datatypes == base_datatypes_count, 'Installing emboss added new datatypes.'
    def test_0025_verify_installed_repository_metadata( self ):
        '''Verify that resetting the metadata on an installed repository does not change the metadata.'''
        self.verify_installed_repository_metadata_unchanged( 'emboss_0030', common.test_user_1_name )
