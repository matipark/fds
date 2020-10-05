//setting up the GET Request 

using System.IO;
using System.IO.Compression;
using System.Net;
using System.Xml;
class MyXMLParser
{
[System.STAThread]
static void Main(string [] args)
{
// setup the request
 HttpWebRequest req = (HttpWebRequest)WebRequest.Create(
"https://datadirect-beta.factset.com/services/TickHistory?" +
"id=FDS-USA&format=xml" +
"&date=20170914&fields=LAST_1,LAST_TIME_1,LAST_VOL_1" +
"&interval=1H&st=100000&et=130000"
 req.KeepAlive = false ;
 req.Headers.Add("Accept-Encoding", "deflate, gzip");
 req.Headers.Add("Authorization", "Basic AaBbCcDdEeFfGgHhIi1234==");
 // make request and get the response
 HttpWebResponse rsp = (HttpWebResponse)req.GetResponse();
 Stream stream = rsp.GetResponseStream();
 // uncompress the response
 If (rsp.ContentEncoding.Equals("deflate"))
 stream = new DeflateStream(stream, CompressionMode.Decompress);
 else if (rsp.ContentEncoding.Equals("gzip"))
 stream = new GZipStream(stream, CompressionMode.Decompress);
 .
 .
 .
//parsing the reponse

XmlTextReader reader = new XmlTextReader(stream);
reader.WhitespaceHandling = WhitespaceHandling.None;
 while (reader.Read())
 {
 if (reader.NodeType.Equals(XmlNodeType.Element))
 {
 if (reader.Name.Equals(“Error”))
 {
 System.Console.WriteLine(reader.Name);
 printAttributes(reader);
 System.Console.WriteLine();
 }
 else if (reader.Name.Equals(“Records”))
 {
 System.Console.WriteLine(reader.Name);
 printAttributes(reader);
 }
 else if (reader.Name.Equals(“Record”))
 {
 System.Console.WriteLine(reader.Name);

 // Move to first Field element
 while (reader.Read() && !reader.Name.Equals("Field"))
 { }

 // Print out all field ids, names and values
 do
 {
 printAttributes(reader);
 } while (reader.Read() && reader.Name.Equals("Field"));
 System.Console.WriteLine();
 }
 }
 }
}
static void printAttributes(XmlTextReader reader)
{
while (reader.MoveToNextAttribute())
 System.Console.Write(reader.Name + ": " + reader.Value + ", ");
System.Console.WriteLine();
}
} // class MyXmlParser

​