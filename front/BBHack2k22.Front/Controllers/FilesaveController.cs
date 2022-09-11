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
}