## Describes the module(tests) that tests the different functions contained in the project
from destral import testing
from osv import osv
import unittest
from destral.transaction import Transaction
from destral.patch import PatchNewCursors
from datetime import datetime, timedelta
import wizard
import os
import base64
#from mock import patch,Mock
# @author Ikram Ahdadouche El Idrissi
# @author Dalila Jbilou Kouhous

## Testing functions

## Module that tests the configutations, specifically passwords
class ConfiguracioTests(testing.OOTestCase):

    ## Functiom that set up all the module dependencies
        # @param self The object pointer

    def setUp(self):
        self.pool = self.openerp.pool
        self.Configuracio = self.pool.get('som.crawlers.config')
        self.Data = self.pool.get('ir.model.data')
        self.task = self.pool.get('som.crawlers.task')
        self.taskStep = self.pool.get('som.crawlers.task.step')
        self.result = self.pool.get('som.crawlers.result')
        self.wiz= self.pool.get('wizard.executar.tasca')

    def tearDown(self):
        pass

    ## Function that tests if the new password is the same as the old one
        # @param self The object pointe
    def test_canviarContrasenya_contrasenya_nova_igual_contrasenya_antiga_resultat_exception(self):
        with Transaction().start(self.database) as txn:
            cursor = txn.cursor
            uid = txn.user
            #get_object_reference per llegir la id de un objecte

            crawler_config_id = self.Data.get_object_reference(cursor, uid, 'som_crawlers', 'demo_configuracio_1')[1]
            #set values
            password = 'Admin'
            #check result
            result = self.Configuracio.canviar_contrasenya(cursor,uid,crawler_config_id,password)
            with self.assertRaises(osv.except_osv) as context:
                self.Configuracio.canviar_contrasenya(cursor,uid,crawler_config_id,password)

            self.assertTrue('Contrasenya identica a la anterior!','Torna a introduir una contrasenya diferent a la anterior' in context.exception)

    ## Function that tests if the modification password gets an ok result
        # @param self The object pointer
    def test_canviarContrasenya_nova_resultat_ok(self):
            with Transaction().start(self.database) as txn:
                cursor = txn.cursor
                uid = txn.user
                #get_object_reference per llegir la id de un objecte
                crawler_config_id = self.Data.get_object_reference(cursor, uid, 'som_crawlers', 'demo_configuracio_1')[1]
                #set values
                password = 'Hola'
                #try test
                result = self.Configuracio.canviar_contrasenya(cursor,uid,crawler_config_id,password)
                #check result
                self.assertEqual(result, password)
                #objecte.browse(... + id) per llegir el objecte al complet.


# Module that tests the executar tasca wizard
class WizardExecutarTascaTests(testing.OOTestCase):
    ## Functiom that set up all the module dependencies
        # @param self The object pointer
    def setUp(self):
        self.pool = self.openerp.pool
        self.Configuracio = self.pool.get('som.crawlers.config')
        self.Data = self.pool.get('ir.model.data')
        self.task = self.pool.get('som.crawlers.task')
        self.taskStep = self.pool.get('som.crawlers.task.step')
        self.result = self.pool.get('som.crawlers.result')              
        self.wiz= self.pool.get('wizard.executar.tasca')

    def tearDown(self):
        pass
    
    """Function that tests if after trying to download files, the result is "Falta especificar nom fitxer"
        # @param self The object pointer"""
    def test_download_files_resultat_falta_especificar_nomfitxer(self): #no detecta l'id que toca??

        with Transaction().start(self.database) as txn:
                cursor = txn.cursor
                uid = txn.user
                crawler_task_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_accions_planificades_1')[1]
                crawler_task_step_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_taskStep_3')[1]
                #set values
                result_id = self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_result_1')[1]
                #try test
                resultat = self.taskStep.download_files(cursor, uid,crawler_task_step_id, result_id)
                #check result
                self.assertEqual(resultat, 'Falta especificar nom fitxer')
               

    """Function that tests if after trying to download files, the result is that the directory does not exits
        # @param self The object pointer"""
    def test_download_files_resultat_file_or_directory_does_not_exist(self):
         with Transaction().start(self.database) as txn:
                cursor = txn.cursor
                uid = txn.user
                crawler_task_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_accions_planificades_1')[1]
                crawler_task_step_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_taskStep_5')[1]
                #set values
                result_id = self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_result_1')[1]
                #try test
                
                result = self.taskStep.download_files(cursor, uid,crawler_task_step_id,result_id)
                #check result
                self.assertEqual(result, 'File or directory doesn\'t exist')
                #objecte.browse(... + id) per llegir el objecte al complet.

    def no_test_download_files_resultat_files_has_been_succesfully_downloaded(self):
        with Transaction().start(self.database) as txn:
                cursor = txn.cursor
                uid = txn.user
                crawler_task_step_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_taskStep_1')[1]
                #try test
                result_id = self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_result_1')[1]
                #try test
                result = self.taskStep.download_files(cursor, uid,crawler_task_step_id,result_id)
                #check result
                self.assertEqual(result, 'files succesfully attached')
                #objecte.browse(... + id) per llegir el objecte al complet.

    #import_xml_files

    """Import xml test --> id does not exist
        # @param self The object pointer"""
    def test_import_xml_files_resultat_task_step_id_does_not_exist(self):
            with Transaction().start(self.database) as txn:
                cursor = txn.cursor
                uid = txn.user
                crawler_task_step_id = self.Data.get_object_reference(cursor, uid, 'som_crawlers', 'demo_taskStep_6')[1]
                #try test
                result_id = self.Data.get_object_reference(cursor, uid, 'som_crawlers', 'demo_result_2')[1]
                with self.assertRaises(Exception) as context:
                    self.taskStep.import_xml_files(cursor, uid, crawler_task_step_id, result_id)
                #check result
                self.assertTrue('don\'t exist id attachment' in context.exception)

       
    def test_import_xml_files_entrada_zip_prova_sortida_import_donee(self): 
        with Transaction().start(self.database) as txn:
            cursor = txn.cursor
            uid = txn.user
            #set values
            crawler_taskStep_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_taskStep_8')[1]
            crawler_taskStep_obj = self.taskStep.browse(cursor,uid,crawler_taskStep_id)
            result_id = self.Data.get_object_reference(cursor, uid, 'som_crawlers', 'demo_result_4')[1]
            pathToZip = "~/openerp_som_addons/som_crawlers/demo/zip_demo_2/anselmo_2022-07-26_15_11_GRCW_W4X151_20220726151137.zip"
            with open(pathToZip ,'rb') as f:
                content  = f.read()
            attachment = {
                        'name':  "anselmo_2022-07-26_15_11_GRCW_W4X151_20220726151137.zip",
                        'datas':  base64.b64encode(content),
                        'datas_fname': "anselmo_2022-07-26_15_11_GRCW_W4X151_20220726151137.zip",
                        'res_model': 'som.crawlers.task',
                        'res_id': crawler_taskStep_obj.task_id.id,
                    }

            attachment_id = self.pool.get('ir.attachment').create(cursor, uid, attachment, context=None)
            result.write(cursor,uid, result_id, {'zip_name': attachment_id})
            result = self.taskStep.import_xml_files(cursor,uid,crawler_taskStep_id,result_id) #'som.crawler.task.step' import_wizard
            self.assertEqual(result,'Successful import') 
            
    def no_test_executar_una_tasca(self):
         with Transaction().start(self.database) as txn:
            cursor = txn.cursor
            uid = txn.user
            crawler_task_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_accions_planificades_1')[1]
            result = self.wiz.executar_tasca(cursor,uid,crawler_task_id,context=None)
            #check result --> comparacio
            self.assertEqual(result,{'type': 'ir.actions.act_window_close'})

    # id del portal config
    """ Id portal config tests --> suucessful result
        # @param self The object pointer"""
    def test_id_del_portal_config_entrada_prova_sortida_prova_success(self):
        with Transaction().start(self.database) as txn:
            cursor = txn.cursor
            uid = txn.user
            crawler_task_id = self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_accions_planificades_2')[1]
            crawler_config_id = self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_configuracio_2')[1]
            crawler_config_obj = self.Configuracio.browse(cursor, uid, crawler_config_id)
            result = self.task.id_del_portal_config(cursor,uid,crawler_task_id)
            self.assertEqual(result,crawler_config_obj)
        
    """ Id portal config tests --> error result
        # @param self The object pointer"""
    def test_id_del_portal_config_entrada_anselmo_sortida_prova_i_error(self):
        with Transaction().start(self.database) as txn:
            cursor = txn.cursor
            uid = txn.user
            crawler_task_id = self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_accions_planificades_1')[1]
            crawler_config_id = self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_configuracio_2')[1]
            crawler_config_obj = self.Configuracio.browse(cursor, uid, crawler_config_id)
            result = self.task.id_del_portal_config(cursor,uid,crawler_task_id)
            self.assertNotEqual(result,crawler_config_obj)

    """Attach file test --> directory does not exist
        # @param self The object pointer"""
    def test_attach_files_zip_entrada_path_inexistent_sortida_zip_directory_no_existeix(self):
        with Transaction().start(self.database) as txn:
            cursor = txn.cursor
            uid = txn.user
            crawler_taskStep_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_taskStep_1')[1]
            crawler_config_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_configuracio_1')[1]
            result_id = self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_result_2')[1]
            crawler_config_obj = self.Configuracio.browse(cursor,uid,crawler_config_id)
            pathFileActual = os.path.dirname(os.path.realpath(__file__))
            result = self.taskStep.attach_files_zip(cursor, uid, crawler_taskStep_id, result_id, crawler_config_obj, pathFileActual, context=None)
            self.assertEqual(result,'zip directory doesn\'t exist')

    """Attach files zip tests --> directori es buit.
        # @param self The object pointer"""
    def test_attach_files_zip_entrada_directory_buit_sortida_zip_directory_buit(self):
        with Transaction().start(self.database) as txn:
            cursor = txn.cursor
            uid = txn.user
            crawler_taskStep_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_taskStep_1')[1]
            crawler_config_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_configuracio_1')[1]
            result_id = self.Data.get_object_reference(cursor, uid, 'som_crawlers', 'demo_result_2')[1]
            crawler_config_obj = self.Configuracio.browse(cursor,uid,crawler_config_id)
            pathFileActual = os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')
            result = self.taskStep.attach_files_zip(cursor, uid, crawler_taskStep_id, result_id, crawler_config_obj, pathFileActual, context=None)

            self.assertEqual(result,'Directori doesn\'t contain any ZIP')
            
    """ Attach files zip test --> file successfully attached
        # @param self The object pointer"""
    def test_attach_files_zip_entrada_config_prova_sortida_files_successfuly_attached(self): # si que dona ok, pero al no tenir el zip donara fail pq fem remove
        with Transaction().start(self.database) as txn:
            cursor = txn.cursor
            uid = txn.user
            result_id = self.Data.get_object_reference(cursor, uid, 'som_crawlers', 'demo_result_3')[1]
            crawler_config_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_configuracio_3')[1]
            crawler_taskStep_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_taskStep_8')[1]
            crawler_config_obj = self.Configuracio.browse(cursor,uid,crawler_config_id)
            pathFileActual = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../demo')
            result = self.taskStep.attach_files_zip(cursor, uid, crawler_taskStep_id, result_id, crawler_config_obj, pathFileActual, context=None)
            self.assertEqual(result,'files succesfully attached')
    
    """  Create args for script test --> sortida string arguments
         # @param self The object pointer"""
    def test_createArgsForScript_entrada_config_prova_sortida_string_arguments(self):
        with Transaction().start(self.database) as txn:
            cursor = txn.cursor
            uid = txn.user
            crawler_config_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_configuracio_4')[1]
            crawler_taskStep_id= self.Data.get_object_reference(cursor,uid,'som_crawlers','demo_taskStep_9')[1]
            
            crawler_config_obj = self.Configuracio.browse(cursor,uid,crawler_config_id)
            fileName = "prova.txt"
            result = self.taskStep.createArgsForScript(cursor,uid,crawler_taskStep_id,crawler_config_obj,fileName)
            result_string ="-u  Hola  -d 5 -f prova.txt -url https://egymonluments.gov.eg/en/museums/egyptian-museum  -p  ***  -c Selenium -b firefox -n Tutankamon -fltr  https://egymonuments.gov.eg/en/collections/kawit-sarcophagus-4  -nfp False"
            
            self.assertEqual(result,result_string)

