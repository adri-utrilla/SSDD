"""Authentication service application."""

import logging
import sys
from typing import List
import threading
import time

import Ice
# pylint: disable=E0401
import IceDrive
import IceStorm



from icedrive_blob.blob import BlobService
#from icedrive_blob.blob import DataTransfer
from icedrive_blob.discovery import Discovery


class BlobApp(Ice.Application):
    """Implementation of the Ice.Application for the Blob service."""

    def run(self, args: List[str]) -> int:
        """Execute the code for the BlobApp class."""
        properties = self.communicator().getProperties()
        topic_name = properties.getProperty("DiscoveryTopic")
        topic_manager = IceStorm.TopicManagerPrx.checkedCast(
            self.communicator().propertyToProxy("IceStorm.TopicManager.Proxy"))

        try:
            topic = topic_manager.retrieve(topic_name)
        except IceStorm.NoSuchTopic:
            topic = topic_manager.create(topic_name)

        adapter = self.communicator().createObjectAdapter("BlobAdapter")
        adapter.activate()

        discovery_pub = IceDrive.DiscoveryPrx.uncheckedCast(topic.getPublisher())

        blob_directory = self.communicator().getProperties().getProperty("ArchivesDirectory")

        discovery_servant = Discovery()
        discovery_proxy = adapter.addWithUUID(discovery_servant)

        servant = BlobService(blob_directory, discovery_proxy)
        servant_proxy = adapter.addWithUUID(servant)

        logging.info("Proxy Blob: %s", servant_proxy)

        blob_proxy = IceDrive.BlobServicePrx.uncheckedCast(servant_proxy)

        #self.send_announcement(discovery_pub, blob_proxy)

        blob_thread = threading.Thread(
            target=self.send_announcement, args=(discovery_pub, blob_proxy), daemon=True)
        blob_thread.start()


        topic.subscribeAndGetPublisher({},discovery_proxy)

        #DataTransferServant = DataTransfer("/home/adrian/SSDD/PClase1/Cliente.py")
        #DtServant = adapter.addFacetWithUUID(DataTransferServant)


        #logging.info("Proxy Dt: %s", DtServant)


        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0
    
    def send_announcement(self, publisher, service_prx):
        """Metodo que envia anunciamientos durante 5 segundos"""
        while True:
            publisher.announceBlobService(service_prx)
            time.sleep(5)


def main():
    """Handle the icedrive-authentication program."""
    app = BlobApp()
    return app.main(sys.argv)
