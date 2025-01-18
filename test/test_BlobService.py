from icedrive_blob.blob import DataTransfer
from icedrive_blob.blob import BlobService
from tempfile import NamedTemporaryFile
import pytest

import IceDrive


def test_data_transfer_creation_fail():
    with pytest.raises(Exception):
        DataTransfer("ruta/inventada")

def test_data_transfer_read():
    dt = DataTransfer("prueba.txt")
    data = b""
    while True:
        chunk = dt.read(1024)
        if not chunk:
            break
        data += chunk
    assert data == b"Hola mundo"

def test_blob_service_link_success():
    bs = BlobService()
    blobId = "BlobIDPruebaLink"
    bs.links[blobId] = 0
    bs.link(blobId)
    assert bs.links[blobId] == 1

def test_blob_sercice_link_fail():
    bs = BlobService()
    blobID = "BlobID_NO_EXISTE"
    with pytest.raises(IceDrive.UnknownBlob, match=blobID):
        bs.link(blobID)

def test_blob_service_unlink_success():
    bs = BlobService()
    blobID = "BlobIDPruebaUnlink"
    bs.links[blobID] = 2
    bs.unlink(blobID)
    assert bs.links[blobID] == 1

def test_blob_service_upload():
    bs = BlobService()
    #ruta = input("Escribe la ruta del archivo que quieras subir")
    dt = DataTransfer("/home/adrian/SSDD/PClase1/Cliente.py")
    hashResultado = bs.upload(dt)
    hashPrueba = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert hashResultado == hashPrueba  


def test_blob_sercice_download_fail():
    bs = BlobService()
    blobID = "BlobID_NO_EXISTE"
    with pytest.raises(IceDrive.UnknownBlob, match=blobID):
        bs.download(blobID)

