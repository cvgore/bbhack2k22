using System.Net.Http.Headers;
using System.Text.Json;
using BBHack2k22.Front.Models;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Forms;
using Microsoft.JSInterop;

namespace BBHack2k22.Front.Pages;

public partial class Index
{
    public FormModel FormModel { get; set; } = new() { ImgFiles = new(), TranslationFiles = new() };
    private List<string> fileNames = new();
    private List<UploadResult> _uploadResults = new();
    long maxFileSize = 1024 * 1 * 1_000_000;

    private async Task OnInputTranslationFileChange(InputFileChangeEventArgs e)
    {
        foreach (var file in e.GetMultipleFiles(e.FileCount))
        {
            FormModel.TranslationFiles.Add(file);
        }
    }

    private async Task OnInputImageFileChange(InputFileChangeEventArgs e)
    {
        foreach (var file in e.GetMultipleFiles(e.FileCount))
        {
            FormModel.ImgFiles.Add(file);
        }
    }

    private async Task Submit()
    {
        try
        {
            using var content = new MultipartFormDataContent();
            foreach (var file in FormModel.ImgFiles)
            {
                var fileContent2 = new StreamContent(file.OpenReadStream(maxFileSize));
                fileContent2.Headers.ContentType = new MediaTypeHeaderValue(file.ContentType);
                fileNames.Add(file.Name);

                content.Add(content: fileContent2, name: "\"ImgFiles\"", fileName: file.Name);
            }
            foreach (var file in FormModel.TranslationFiles)
            {
                var fileContent = new StreamContent(file.OpenReadStream(maxFileSize));
                fileContent.Headers.ContentType = new MediaTypeHeaderValue(file.ContentType);
                fileNames.Add(file.Name);

                content.Add(content: fileContent, name: "\"TranslationFiles\"", fileName: file.Name);
            }
            var response = await Client.PostAsync("http://localhost:5072/api/Filesave", content);
            if (response.IsSuccessStatusCode)
            {
                var baseString = await response.Content.ReadAsStringAsync();

                byte[] bytesStream = Convert.FromBase64String(baseString);
                FileStream stream = new FileStream(@"Front/pdfFiles", FileMode.CreateNew);
                BinaryWriter writer = new BinaryWriter(stream);
                writer.Write(bytesStream, 0, bytesStream.Length);
                writer.Close();

                await jsRuntime.InvokeVoidAsync("downloadFile", "application/zip", baseString, "test.zip");
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
            throw;
        }
    }

    private string? GetStoredFiles(string fileName)
    {
        var uploadResult = _uploadResults.FirstOrDefault(x => x.FileName == fileName);
        return uploadResult?.StoredFileName ?? "Filed not found";
    }
}