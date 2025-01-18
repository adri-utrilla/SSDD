import sys
import Ice
Ice.loadSlice("icedrive.ice")
import IceDrive

class Client(Ice.Application):
    
    def run(self, argv):
        prx = self.communicator().stringToProxy(argv[1])
        blobService = IceDrive.BlobServicePrx.checkedCast(prx)
        dataTransfer = IceDrive.DataTransferPrx.checkedCast(prx)
        blob = IceDrive.BlobServicePrx.checkedCast(prx)

        if not blobService and not blob:
            raise RuntimeError("Invalid Proxy")
        else:
            while True:
                option = input("1- Link file\n" +
                               "2- Unlink file\n" + 
                               "3- Upload file\n" + 
                               "4- Download file\n" +
                               "E- Exit\n\n" +
                               "\tOpcion: ")
                if option == str(1):
                    bs = blobService()
                    blobId = "BlobPruebaLink"
                    bs.links[blobId] = 0
                    bs.link(blobId)
                    print("El numero de veces que esta enlazado ese BlobID es " + bs.links[blobId])
                elif option == str(2):
                    bs = blobService()
                    blobId = "BlobPruebaUnlink"
                    bs.links[blobId] = 2
                    bs.unlink(blobId)
                    print("El numero de veces que esta enlazado ese BlobId es " +bs.links[blobId])
                elif option == str(3):
                    bs = blobService()
                    dt = dataTransfer("/home/adrian/SSDD/PClase1/Cliente.py")
                    hashR = bs.upload(dt)
                    print("Se ha subido el archivo" + hashR)
                elif option == 'E':
                    break

client = Client()
sys.exit(client.main(sys.argv))

