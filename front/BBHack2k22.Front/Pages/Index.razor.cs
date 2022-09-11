using System.Net.Http.Headers;
using System.Text.Json;
using BBHack2k22.Front.Models;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Forms;

namespace BBHack2k22.Front.Pages;

public partial class Index
{
    // public FormModel FormModel { get; set; } = new();
    //
    // [Inject]
    // private ILogger<Index> Logger { get; set; }
    // private List<string> fileNames = new();
    //
    // private async Task OnInputFileChange(InputFileChangeEventArgs e)
    // {
    //     long maxFileSize = 1024 * 1 * 1_000_000;
    //     using var content = new MultipartFormDataContent();
    //     foreach (var file in e.GetMultipleFiles(e.FileCount))
    //     {
    //         var fileContent = new StreamContent(file.OpenReadStream(maxFileSize));
    //         fileContent.Headers.ContentType = new MediaTypeHeaderValue(file.ContentType);
    //         fileNames.Add(file.Name);
    //         
    //         content.Add(content: fileContent, name: "\"files\"", fileName: file.Name);
    //     }
    //     
    //     // shouldRender = false;
    //     // long maxFileSize = 1024 * 1 * 1_000_000;
    //     // var upload = false;
    //     //
    //     // using var content = new MultipartFormDataContent();
    //     //
    //     // foreach (var file in e.GetMultipleFiles(e.FileCount))
    //     // {
    //     //     if (uploadResults.SingleOrDefault(
    //     //         f => f.FileName == file.Name) is null)
    //     //     {
    //     //         try
    //     //         {
    //     //             var fileContent = 
    //     //                 new StreamContent(file.OpenReadStream(maxFileSize));
    //     //
    //     //             // fileContent.Headers.ContentType = 
    //     //             //     new MediaTypeHeaderValue(file.ContentType);
    //     //
    //     //             files.Add(new() { Name = file.Name });
    //     //
    //     //             content.Add(
    //     //                 content: fileContent,
    //     //                 name: "\"files\"",
    //     //                 fileName: file.Name);
    //     //             
    //     //             upload = true;
    //     //         }
    //     //         catch (Exception ex)
    //     //         {
    //     //             Logger.LogInformation(
    //     //                 "{FileName} not uploaded (Err: 6): {Message}", 
    //     //                 file.Name, ex.Message);
    //     //
    //     //             uploadResults.Add(
    //     //                 new()
    //     //                 {
    //     //                     FileName = file.Name, 
    //     //                     ErrorCode = 6, 
    //     //                     Uploaded = false
    //     //                 });
    //     //         }
    //     //     }
    //     // }
    //     //
    //     // if (upload)
    //     // {
    //     //     var client = ClientFactory.CreateClient();
    //     //
    //     //     var response = 
    //     //         await client.PostAsync("http://localhost:5072/Filesave", 
    //     //         content);
    //     //
    //     //     if (response.IsSuccessStatusCode)
    //     //     {
    //     //         var options = new JsonSerializerOptions
    //     //         {
    //     //             PropertyNameCaseInsensitive = true,
    //     //         };
    //     //
    //     //         using var responseStream =
    //     //             await response.Content.ReadAsStreamAsync();
    //     //
    //     //         var newUploadResults = await JsonSerializer
    //     //             .DeserializeAsync<IList<UploadResult>>(responseStream, options);
    //     //
    //     //         if (newUploadResults is not null)
    //     //         {
    //     //             uploadResults = uploadResults.Concat(newUploadResults).ToList();
    //     //         }
    //     //     }
    //     // }
    //     //
    //     // //shouldRender = true;
    // }
}