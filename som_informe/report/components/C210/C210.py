from gestionatr.utils import get_description
from ..component_utils import dateformat
from ..ProcesC2 import ProcesC2

class C210(ProcesC2.ProcesC2):
    def __init__(self):
        ProcesC2.ProcesC2.__init__(self)

    def get_data(self, wiz, cursor, uid, step):
        result = ProcesC2.ProcesC2.get_data(self, wiz, cursor, uid, step)
        result['type'] = 'C210'
        result['data_creacio'] = dateformat(step.date_created)
        result['data_acceptacio'] = dateformat(step.data_acceptacio)

        return result