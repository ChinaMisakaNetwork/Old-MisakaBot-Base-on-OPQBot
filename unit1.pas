unit Unit1;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, mysql51conn, SQLDB, Forms, Controls, Graphics,
  Dialogs, StdCtrls, DCPsha256;

type

  { TForm1 }

  TForm1 = class(TForm)
    Button1: TButton;
    Button2: TButton;
    DCP_sha256_1: TDCP_sha256;
    Edit1: TEdit;
    Edit2: TEdit;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    MySQL51Connection1: TMySQL51Connection;
    SQLQuery1: TSQLQuery;
    SQLTransaction1: TSQLTransaction;
    procedure Button1Click(Sender: TObject);
    procedure Button2Click(Sender: TObject);
    procedure Edit1Change(Sender: TObject);
    procedure Edit1Click(Sender: TObject);
    procedure Edit1KeyPress(Sender: TObject; var Key: char);
    procedure Edit2Change(Sender: TObject);
    procedure Edit2KeyPress(Sender: TObject; var Key: char);
    procedure FormClose(Sender: TObject; var CloseAction: TCloseAction);
    procedure FormCreate(Sender: TObject);
    procedure FormShow(Sender: TObject);
  private

  public

  end;

var
  Form1: TForm1;
  conn: TMySQL51Connection;
  query: TSQLQuery;
  transaction: TSQLTransaction;
  Priv: integer;
  lft: integer;
  top: integer;
const
  st1: String= '81.6';
  st2: String= 'Mis';
  st3: String= 'work';
  st4: String= '.129';
  st5: String= 'ak';
  st6: String= 'aNe';
  st7: String= 't';
  st8: String= '8.2';
  st9: String= '45';
implementation

{$R *.lfm}

{ TForm1 }
uses Unit2;
function bintoAscii(const bin: array of byte): AnsiString;
var i: integer;
begin
    SetLength(Result, Length(bin));
    for i := 0 to Length(bin)-1 do
      Result[1+i] := AnsiChar(bin[i]);
end;

function SHA256_2(enc: string): string;
var Hash: TDCP_sha256;
  Digest: array[0..31] of byte;
  Source: string;
  i: integer;
  str1: string;
  anotherstring: string;
begin
    Hash := TDCP_sha256.Create(nil);
    Hash.Init;
    Hash.UpdateStr(enc);
    Hash.Final(Digest);
    anotherstring := bintoAscii(Digest);
    Hash := TDCP_sha256.Create(nil);
    Hash.Init;
    Hash.UpdateStr(anotherstring);
    Hash.Final(Digest);
    for i:= 0 to 31 do str1 := str1 + IntToHex(Digest[i], 2);
    Result := LowerCase(str1);
end;

function login(): integer;
begin
   Form1.Label3.Caption := '';
   if length(Form1.Edit1.Text)=0 then
   begin
     Form1.Label3.Caption := Format('%s%s%s', [Form1.Label3.Caption, 'Missing Username', #13#10]);
     Form1.Label1.Font.Color := clRed;
   end
   else Form1.Label1.Font.Color := clDefault;
   if length(Form1.Edit2.Text)=0 then
   begin
     Form1.Label3.Caption := Format('%s%s%s', [Form1.Label3.Caption, 'Missing Password', #13#10]);
     Form1.Label2.Font.Color := clRed;
   end
   else Form1.Label2.Font.Color := clDefault;
   if (length(Form1.Edit2.Text)=0) or (length(Form1.Edit1.Text)=0) then exit();
   if pos(#39, Form1.Edit1.Text)>0 then
   begin
     Form1.Label3.Caption := Format('%s%s%s', [Form1.Label3.Caption, 'Illegal Characters', #13#10]);
     exit();
   end;
   conn := TMySQL51Connection.Create(nil);
   query := TSQLQuery.Create(nil);
   transaction := TSQLTransaction.Create(nil);
   conn.HostName := Format('%s%s%s%s', [st1,st8,st9,st4]);
   conn.UserName := Format('%s%s%s%s%s', [st2,st5,st6,st7,st3]);
   conn.Password := Format('%s%s%s%s%s', [st2,st5,st6,st7,st3]);
   conn.DatabaseName := Format('%s%s%s%s%s', [st2,st5,st6,st7,st3]);
   conn.Connected := True;
   conn.Transaction := transaction;
   query.DataBase := conn;
   query.SQL.Text := Format('%s%s%s%s%s%s%s', ['select * from WebAdmin where QQ=',Form1.Edit1.Text,' and Pass=',#39,SHA256_2(Form1.Edit2.Text),#39,';']);
   query.Open;
   query.Last;
   if query.RecordCount = 0 then
   begin
     Form1.Label3.Caption := 'Username of Password Error';
     exit();
   end
   else
   begin
     Priv := query.FieldByName('Priv').AsInteger;
     Unit2.Priv := Priv;
     Unit2.Username := Form1.Edit1.Text;
     Form1.Edit1.Text := '';
     Form1.Edit2.Text := '';
     Form1.Label3.Caption := '';
     query.Free;
     conn.Free;
     Form1.hide();
     Unit2.lft := Form1.Left;
     Unit2.top := Form1.Top;
     Unit2.Form2.Show();
     exit();
   end;
   query.Free;
   conn.Free;
end;

procedure TForm1.FormCreate(Sender: TObject);
begin

end;

procedure TForm1.FormShow(Sender: TObject);
begin
  Form1.Top := top;
  Form1.Left := lft;
end;

procedure TForm1.Edit1Change(Sender: TObject);
begin

end;

procedure TForm1.Edit1Click(Sender: TObject);
begin

end;

procedure TForm1.Edit1KeyPress(Sender: TObject; var Key: char);
begin
  if (Key = #10) or (Key = #13) then login();
end;

procedure TForm1.Button1Click(Sender: TObject);
begin
  login();
end;

procedure TForm1.Button2Click(Sender: TObject);
begin
  Application.Terminate;
end;

procedure TForm1.Edit2Change(Sender: TObject);
begin

end;

procedure TForm1.Edit2KeyPress(Sender: TObject; var Key: char);
begin
   if (Key = #10) or (Key = #13) then login();
end;

procedure TForm1.FormClose(Sender: TObject; var CloseAction: TCloseAction);
begin
  Application.Terminate();
end;

end.

