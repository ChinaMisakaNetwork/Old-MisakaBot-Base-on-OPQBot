unit Unit3;

{$mode objfpc}{$H+}

interface

uses
  Classes, SysUtils, SQLDB, mysql51conn, Forms, Controls, Graphics, Dialogs,
  StdCtrls, DCPsha256;

type

  { TForm3 }

  TForm3 = class(TForm)
    Button1: TButton;
    CheckBox1: TCheckBox;
    CheckBox2: TCheckBox;
    CheckBox3: TCheckBox;
    DCP_sha256_1: TDCP_sha256;
    Edit1: TEdit;
    Label1: TLabel;
    Label2: TLabel;
    Label3: TLabel;
    Label4: TLabel;
    Label5: TLabel;
    MySQL51Connection1: TMySQL51Connection;
    SQLQuery1: TSQLQuery;
    procedure Button1Click(Sender: TObject);
    procedure FormActivate(Sender: TObject);
    procedure FormClose(Sender: TObject; var CloseAction: TCloseAction);
    procedure FormShow(Sender: TObject);
  private

  public

  end;

var
  Form3: TForm3;
  Priv: Integer;
  Username: String;
  conn: TMySQL51Connection;
  query: TSQLQuery;
  transaction: TSQLTransaction;
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
uses Unit2, Unit1;
{$R *.lfm}

{ TForm3 }
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
procedure TForm3.FormActivate(Sender: TObject);
begin
  Label5.Caption := Username;
  CheckBox1.Checked := Boolean((Priv div 4) mod 2);
  CheckBox1.Enabled := Boolean((Priv div 4) mod 2);
  CheckBox2.Checked := Boolean((Priv div 2) mod 2);
  CheckBox2.Enabled := Boolean((Priv div 2) mod 2);
  CheckBox3.Checked := Boolean((Priv) mod 2);
  CheckBox3.Enabled := Boolean((Priv) mod 2);
end;

procedure TForm3.Button1Click(Sender: TObject);
begin
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
   if length(Edit1.Text) > 0 then
   begin
        query.SQL.Text := 'update WebAdmin set Pass="' +SHA256_2(Edit1.Text) + '" where QQ=' + Username + ';';
        Edit1.Text := '';
        query.ExecSQL;
        transaction.Commit;
   end;
   query.Free();
   conn.Free();
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
   Priv := 0;
   if (CheckBox3.Checked = true) then Priv := Priv + 1;
   if (CheckBox2.Checked = true) then Priv := Priv + 2;
   if (CheckBox1.Checked = true) then Priv := Priv + 4;
   query.SQL.Text := 'update WebAdmin set Priv="' + IntToStr(Priv) + '" where QQ=' + Username + ';';
   query.ExecSQL;
   transaction.Commit;
   query.Free();
   conn.Free();
end;

procedure TForm3.FormClose(Sender: TObject; var CloseAction: TCloseAction);
begin
  Username := '';
  Priv := 0;
  Unit2.top := Form3.Top + 42;
  Unit2.lft := Form3.Left + 12;
  Unit2.Form2.show;
end;

procedure TForm3.FormShow(Sender: TObject);
begin
  Form3.Top := top - 42;
  Form3.Left := lft - 12;
end;

end.

