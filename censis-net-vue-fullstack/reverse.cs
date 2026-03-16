// Online C# Editor for free
// Write, Edit and Run your C# code using C# Online Compiler

using System;

public class HelloWorld
{
    public static void Main(string[] args)
    {
        Console.WriteLine ("Try programiz.pro");
        string sentence = " hello world";
        // output "olleh dlrow"
        
        string[] words = sentence.Split(" ");
        
        // loop all the words
            // get the reverese of the word
            // update the word
        string result = "";
        
        foreach(string word in words)
        {
            string reverseWord = Reverse(word);
            // result += reverseWord;
            result = result + " " + reverseWord;
            
            
        }
        
        result = result.Trim();
        Console.WriteLine (result);
        
        
    }
    
    public static string Reverse(string word)
    {
        // char[] wordArray = []
        // // convert the word as array
        // for(int i =0; i <word.length; i++)
        // {
        //     wordArray.Add(word[])
        // }
        
        
        // int strat = 0;
        // int end = word.length -1;
        
        // while(start<end)
        // {
        //     char temp = word[start]
        //     word[start]
        // }
        
        string reserseWord = "";
        
        for(int i =word.Length -1; i >=0; i--)
        {
            reserseWord += word[i];
        }
        return reserseWord;
        
    }
}