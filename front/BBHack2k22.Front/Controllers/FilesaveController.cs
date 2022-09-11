using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Http.Headers;
using System.Threading.Tasks;
using BBHack2k22.Front.Models;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;

[ApiController]
[Route("api/[controller]")]
public class FilesaveController : ControllerBase
{
    private readonly IWebHostEnvironment env;
    private readonly ILogger<FilesaveController> logger;
    private readonly IHttpClientFactory _clientFactory;

    public FilesaveController(IWebHostEnvironment env,
        ILogger<FilesaveController> logger, IHttpClientFactory clientFactory)
    {
        this.env = env;
        this.logger = logger;
        _clientFactory = clientFactory;
    }

    [HttpPost]
    public async Task<IActionResult> PostFile([FromForm] List<IFormFile> fileList)
    {
        long maxFileSize = 1024 * 1 * 1_000_000;
        var imagesList = Request.Form.Files.Where(x => x.Name == "ImgFiles").ToList();
        var translationList = Request.Form.Files.Where(x => x.Name == "TranslationFiles").ToList();
        
        
        using var content = new MultipartFormDataContent();
        foreach (var file in imagesList)
        {
            var fileContent2 = new StreamContent(file.OpenReadStream());
            fileContent2.Headers.ContentType = new MediaTypeHeaderValue(file.ContentType);

            content.Add(content: fileContent2, name: "images", fileName: file.Name);
        }
        foreach (var file in translationList)
        {
            var fileContent = new StreamContent(file.OpenReadStream());
            fileContent.Headers.ContentType = new MediaTypeHeaderValue(file.ContentType);

            content.Add(content: fileContent, name: "translation", fileName: file.Name);
        }

        var client = _clientFactory.CreateClient();
        
        var response = await client.PostAsync("http://localhost:6000/" , content);
        if (response.IsSuccessStatusCode)
        {
            
        }

        return new CreatedResult("",new {});
    }
    
    // [HttpPost("xd")]
    // public async Task<ActionResult<List<UploadResult>>> PostFile2(
    //     [FromForm] IEnumerable<IFormFile> files)
    // {
    //     var maxAllowedFiles = 3;
    //     long maxFileSize = 1024 * 15;
    //     var filesProcessed = 0;
    //     var resourcePath = new Uri($"{Request.Scheme}://{Request.Host}/");
    //     List<UploadResult> uploadResults = new();
    //
    //     foreach (var file in files)
    //     {
    //         var uploadResult = new UploadResult();
    //         string trustedFileNameForFileStorage;
    //         var untrustedFileName = file.FileName;
    //         uploadResult.FileName = untrustedFileName;
    //         var trustedFileNameForDisplay =
    //             WebUtility.HtmlEncode(untrustedFileName);
    //
    //         if (filesProcessed < maxAllowedFiles)
    //         {
    //             if (file.Length == 0)
    //             {
    //                 logger.LogInformation("{FileName} length is 0 (Err: 1)",
    //                     trustedFileNameForDisplay);
    //                 uploadResult.ErrorCode = 1;
    //             }
    //             else if (file.Length > maxFileSize)
    //             {
    //                 logger.LogInformation("{FileName} of {Length} bytes is " +
    //                     "larger than the limit of {Limit} bytes (Err: 2)",
    //                     trustedFileNameForDisplay, file.Length, maxFileSize);
    //                 uploadResult.ErrorCode = 2;
    //             }
    //             else
    //             {
    //                 try
    //                 {
    //                     trustedFileNameForFileStorage = Path.GetRandomFileName();
    //                     var path = Path.Combine(env.ContentRootPath,
    //                         env.EnvironmentName, "unsafe_uploads",
    //                         trustedFileNameForFileStorage);
    //
    //                     await using FileStream fs = new(path, FileMode.Create);
    //                     await file.CopyToAsync(fs);
    //
    //                     logger.LogInformation("{FileName} saved at {Path}",
    //                         trustedFileNameForDisplay, path);
    //                     uploadResult.Uploaded = true;
    //                     uploadResult.StoredFileName = trustedFileNameForFileStorage;
    //                 }
    //                 catch (IOException ex)
    //                 {
    //                     logger.LogError("{FileName} error on upload (Err: 3): {Message}",
    //                         trustedFileNameForDisplay, ex.Message);
    //                     uploadResult.ErrorCode = 3;
    //                 }
    //             }
    //
    //             filesProcessed++;
    //         }
    //         else
    //         {
    //             logger.LogInformation("{FileName} not uploaded because the " +
    //                 "request exceeded the allowed {Count} of files (Err: 4)",
    //                 trustedFileNameForDisplay, maxAllowedFiles);
    //             uploadResult.ErrorCode = 4;
    //         }
    //
    //         uploadResults.Add(uploadResult);
    //     }
    //
    //     return new CreatedResult(resourcePath, uploadResults);
    // }
}