using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Components.Forms;

namespace BBHack2k22.Front.Models;

public class FormModel
{
    [Required]
    public List<IBrowserFile>  ImgFiles { get; set; }
    [Required]
    public List<IBrowserFile>  TranslationFiles { get; set; }
}