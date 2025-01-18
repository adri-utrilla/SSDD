"""Module for servants implementations."""
import hashlib
import json
from tempfile import NamedTemporaryFile
import shutil

import Ice
# pylint: disable=E0401
import IceDrive


class DataTransfer(IceDrive.DataTransfer):
    """Implementation of an IceDrive.DataTransfer interface."""
    def __init__(self, path):
        #self.file_descriptor = open(path, 'rb')

        with open(path, "rb") as file:
            self.file_descriptor = file

    def read(self, size: int, current: Ice.Current = None) -> bytes:
        """Returns a list of bytes from the opened file."""
        data = self.file_descriptor.read(size)
        return data

    def close(self, current: Ice.Current = None) -> None:
        """Close the current opened file"""
        self.file_descriptor.close()


class BlobService(IceDrive.BlobService):
    """Implementation of an IceDrive.BlobService interface."""

    def __init__(self, home, discovery):
        self.home_directory = home
        self.links = {} # key : blob_id, value : int contador
        self.blob_ids = {} # key: blob_id, value : str del path
        self.discovery_service = discovery


    def link(self, blob_id: str, current: Ice.Current = None) -> None:
        """Mark a blob_id file as linked in some directory."""

        if blob_id not in self.links:
            raise IceDrive.UnknownBlob(blob_id)
        else:
            self.links[blob_id] += 1
            self.sync_persistencia_links()

    def unlink(self, blob_id: str, current: Ice.Current = None) -> None:
        """Mark a blob_id as unlinked (removed) from some directory."""

        if blob_id in self.links:
            self.links[blob_id] -=1
            self.sync_persistencia_links()
            if self.links[blob_id] == 0:
                del self.links[blob_id]
                self.sync_persistencia_links()
        else:
            raise IceDrive.UnknownBlob()


    def upload(
        self, user: IceDrive.UserPrx, blob: IceDrive.DataTransferPrx, current: Ice.Current = None
    ) -> str:
        """Register a DataTransfer object to upload a file to the service."""
        upload_auth_prx = self.discovery_service.getAuthenticationPrx()
        if upload_auth_prx is None:
            raise IceDrive.TemporaryUnavailable()
        else:
            if upload_auth_prx.verifyUser(user) == True & user.isAlive():
                file_name = ""
                hash_blob = hashlib.sha256()
                with NamedTemporaryFile('wb', delete=False) as file_descriptor:
                    while True:
                        data = blob.read(1024)
                        file_descriptor.write(data)

                        if not data:
                            break

                        hash_blob.update(data)

                    file_descriptor.close()
                    file_name = file_descriptor.name
                blob_id = hash_blob.hexdigest()

                if blob_id in self.links:
                    return blob_id

                shutil.move(file_name, f"{self.home_directory}/{blob_id}")
                self.links[blob_id] = 0
                self.blob_ids[blob_id] = f"{self.home_directory}/{blob_id}"
                self.sync_persistencia_links()
                return blob_id
            else:
                raise IceDrive.TemporaryUnavailable()

    def download(
        self, user: IceDrive.UserPrx, blob_id: str, current: Ice.Current = None
    ) -> IceDrive.DataTransferPrx:
        """Return a DataTransfer objet to enable the client to download the given blob_id."""
        download_auth_prx = self.discovery_service.getAuthenticationPrx()
        if download_auth_prx is None:
            raise IceDrive.TemporaryUnavailable()
        else:
            if download_auth_prx.verifyUser(user) == True & user.isAlive():
                if blob_id not in self.blob_ids:
                    raise IceDrive.UnknownBlob(blob_id)
                else:
                    path = self.blob_ids[blob_id]
                    dt = DataTransfer(path)
                    adapter = current.adapter
                    obj_id = Ice.stringToIdentity("DataTransfer-"+ blob_id)
                    adapter.add(dt, obj_id)
                    proxy = IceDrive.DataTransferPrx.uncheckedCast(adapter.createProxy(obj_id))
                    self.blob_ids[blob_id] = path
                    self.sync_persistencia_blob()

                    return proxy
            else:
                raise IceDrive.TemporaryUnavailable()

    def sync_persistencia_links(self):
        """Sincronizar persistencia link"""
        with open("persistenciaLinks.json", "w") as persistencia:
            json.dump(self.links, persistencia)

    def sync_persistencia_blob(self):
        """Sincronizar persistencia blob"""
        with open("persistenciaBlob.json", "w") as persistencia:
            json.dump(self.blob_ids, persistencia)

# class Server(Ice.Application):

#     def run(self, argv):
#         print("[BLOB SERVICE] Launching Blob service")
#         adapter = self.communicator().createObjectAdapter("BlobAdapter")
#         servant = BlobService()
#         proxy = adapter.add(servant, Ice.stringToIdentity("BlobService"))
#         print(proxy)
#         adapter.activate()
#         self.shutdownOnInterrupt()
#         sys.stdout.flush()
#         self.communicator().waitForShutdown()

# server = Server()
# sys.exit(server.main(sys.argv))
