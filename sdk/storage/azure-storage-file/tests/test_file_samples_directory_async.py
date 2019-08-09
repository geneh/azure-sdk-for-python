# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import asyncio
try:
    import settings_real as settings
except ImportError:
    import file_settings_fake as settings

from filetestcase import (
    FileTestCase,
    TestMode,
    record
)

SOURCE_FILE = 'SampleSource.txt'


class TestDirectorySamples(FileTestCase):

    connection_string = settings.CONNECTION_STRING

    def setUp(self):
        data = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit"
        with open(SOURCE_FILE, 'wb') as stream:
            stream.write(data)

        super(TestDirectorySamples, self).setUp()

    def tearDown(self):
        if os.path.isfile(SOURCE_FILE):
            try:
                os.remove(SOURCE_FILE)
            except:
                pass

        return super(TestDirectorySamples, self).tearDown()

    #--Begin File Samples-----------------------------------------------------------------

    async def _test_create_directory(self):
        # Instantiate the ShareClient from a connection string
        from azure.storage.file.aio import ShareClient
        share = ShareClient.from_connection_string(self.connection_string, "dirshare")

        # Create the share
        await share.create_share()

        try:
            # Get the directory client
            directory = share.get_directory_client(directory_path="mydirectory")

            # [START create_directory]
            await directory.create_directory()
            # [END create_directory]

            # [START upload_file_to_directory]
            # Upload a file to the directory
            with open(SOURCE_FILE, "rb") as source:
                await directory.upload_file(file_name="sample", data=source)
            # [END upload_file_to_directory]

            # [START delete_file_in_directory]
            # Delete the file in the directory
            await directory.delete_file(file_name="sample")
            # [END delete_file_in_directory]

            # [START delete_directory]
            await directory.delete_directory()
            # [END delete_directory]

        finally:
            # Delete the share
            await share.delete_share()

    def test_create_directory(self):
        if TestMode.need_recording_file(self.test_mode):
            return
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_directory())

    async def _test_create_subdirectories(self):
        # Instantiate the ShareClient from a connection string
        from azure.storage.file.aio import ShareClient
        share = ShareClient.from_connection_string(self.connection_string, "subdirshare")

        # Create the share
        await share.create_share()

        try:
            # Get the directory client
            parent_dir = share.get_directory_client(directory_path="parentdir")

            # [START create_subdirectory]
            # Create the directory
            await parent_dir.create_directory()

            # Create a subdirectory
            subdir = parent_dir.create_subdirectory("subdir")
            # [END create_subdirectory]

            # Upload a file to the parent directory
            with open(SOURCE_FILE, "rb") as source:
                await parent_dir.upload_file(file_name="sample", data=source)

            # Upload a file to the subdirectory
            with open(SOURCE_FILE, "rb") as source:
                await subdir.upload_file(file_name="sample", data=source)

            # [START lists_directory]
            # List the directories and files under the parent directory
            my_list = []
            async for item in parent_dir.list_directories_and_files():
                my_list.append(item)
            print(my_list)
            # [END lists_directory]

            # You must delete the file in the subdirectory before deleting the subdirectory
            await subdir.delete_file("sample")
            # [START delete_subdirectory]
            await parent_dir.delete_subdirectory("subdir")
            # [END delete_subdirectory]

        finally:
            # Delete the share
            await share.delete_share()

    def test_create_subdirectories(self):
        if TestMode.need_recording_file(self.test_mode):
            return
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_subdirectories())

    async def _test_get_subdirectory_client(self):
        # Instantiate the ShareClient from a connection string
        from azure.storage.file.aio import ShareClient
        share = ShareClient.from_connection_string(self.connection_string, "dirtest")

        # Create the share
        await share.create_share()

        try:
            # [START get_subdirectory_client]
            # Get a directory client and create the directory
            parent = share.get_directory_client("dir1")
            await parent.create_directory()

            # Get a subdirectory client and create the subdirectory "dir1/dir2"
            subdirectory = parent.get_subdirectory_client("dir2")
            await subdirectory.create_directory()
            # [END get_subdirectory_client]
        finally:
            # Delete the share
            await share.delete_share()

    def test_get_subdirectory_client(self):
        if TestMode.need_recording_file(self.test_mode):
            return
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_subdirectory_client())
