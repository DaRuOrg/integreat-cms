/*
 * This component renders a file upload field
 */
import { StateUpdater, useState } from "preact/hooks";
import { FilePlus, FileText, Upload, Image } from "preact-feather";
import cn from "classnames";

import { Directory, MediaApiPaths } from "../index";

interface Props {
  directory: Directory;
  setUploadFile: StateUpdater<boolean>;
  apiEndpoints: MediaApiPaths;
  allowedMediaTypes: string;
  mediaTranslations: any;
  submitForm: (event: Event, successCallback: () => void) => any;
  isLoading: boolean;
}
export default function UploadFile({
  directory,
  setUploadFile,
  apiEndpoints,
  allowedMediaTypes,
  mediaTranslations,
  submitForm,
  isLoading,
}: Props) {
  // This state is a buffer which contains the currently selected file (the browser type File)
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  return (
    <div className="flex-auto min-w-0 rounded border border-blue-500 shadow-2xl bg-white">
      <div class="rounded w-full p-4 bg-water-500 font-bold">
        <FilePlus class="inline-block mr-2 h-5" />
        {mediaTranslations.heading_upload_file}
      </div>
      <form
        onSubmit={(event: Event) => submitForm(event, () => setUploadFile(false))}
        action={apiEndpoints.uploadFile}
        className="p-4"
      >
        <input name="parent_directory" type="hidden" value={directory ? directory.id : ""} />
        <label for="file-upload">
          {mediaTranslations.label_file_name}
        </label>
        <div class="flex flex-row gap-2 pt-2">
          <label
            for="file-upload"
            title={mediaTranslations.btn_select_file}
            className={cn(
              "w-full truncate whitespace-nowrap text-white leading-tight font-bold py-3 px-4 m-0 rounded",
              { "cursor-not-allowed bg-gray-500": isLoading },
              { "cursor-pointer bg-gray-500 hover:bg-gray-600": !isLoading && selectedFile },
              { "cursor-pointer bg-blue-500 hover:bg-blue-600": !isLoading && !selectedFile }
            )}
            disabled={isLoading}
          >
            {selectedFile ? (
              <span>
                {selectedFile.type.includes("image") ? (
                  <Image class="mr-1 inline-block h-5" />
                ) : (
                  <FileText class="mr-1 inline-block h-5" />
                )}
                {selectedFile.name}
              </span>
            ) : (
              <span>
                <Upload class="mr-1 inline-block h-5" />
                {mediaTranslations.btn_select_file}
              </span>
            )}
          </label>
          <input
            id="file-upload"
            type="file"
            name="file"
            accept={allowedMediaTypes}
            maxLength={255}
            onChange={({ target }) => setSelectedFile((target as HTMLInputElement).files[0])}
            className="hidden"
            required
            disabled={isLoading}
          />
          <button
            title={mediaTranslations.btn_upload}
            class="btn"
            disabled={!selectedFile || isLoading}
          >
            {mediaTranslations.btn_upload}
          </button>
        </div>
      </form>
    </div>
  );
}
