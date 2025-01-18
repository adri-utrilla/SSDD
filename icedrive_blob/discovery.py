"""Servant implementations for service discovery."""

import Ice
# pylint: disable=E0401
import IceDrive


class Discovery(IceDrive.Discovery):
    """Servants class for service discovery."""
    authenticationSet = set()

    def announceAuthentication(self, prx: IceDrive.AuthenticationPrx, current: Ice.Current = None) -> None:
        """Receive an Authentication service announcement."""

        print("AUTHENTICATION PROX: " + prx)
        self.authenticationSet.add(prx)

    def announceDirectoryService(self, prx: IceDrive.DirectoryServicePrx, current: Ice.Current = None) -> None:
        """Receive an Directory service announcement."""

        print("DIRECTORY SERVICE PROXY: " + prx)

    def announceBlobService(self, prx: IceDrive.BlobServicePrx, current: Ice.Current = None) -> None:
        """Receive an Blob service announcement."""

        print("BLOB SERVICE PROXY: " + prx)

    def get_authentication_prx(self ,current: Ice.Current = None) -> IceDrive.AuthenticationPrx:
        while len(self.authenticationSet) > 0:
            authentication_prx = self.authenticationSet.pop()
            self.authenticationSet.add(authentication_prx)
            try:
                authentication_prx.ice_ping()
                return authentication_prx
            except Ice.Exception:
                self.authenticationSet.remove(authentication_prx)
        return None
