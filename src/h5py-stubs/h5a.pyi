from h5py._base_id import BaseID

class AttrID(BaseID):
    @property
    def name(self) -> str: ...
