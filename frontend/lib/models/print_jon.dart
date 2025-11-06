import 'dart:io';


class PrintJob {
  final String id;
  final String fileName;
  final File file;
  int copies;
  String color;
  String pageSize;
  String comments;

  PrintJob({
    required this.id,
    required this.fileName,
    required this.file,
    this.copies = 1,
    this.color = 'Black & White',
    this.pageSize = 'A4',
    this.comments = '',
  });

  PrintJob copyWith({
    int? copies,
    String? color,
    String? pageSize,
    String? comments,
  }) {
    return PrintJob(
      id: id ?? this.id,
      fileName: fileName ?? this.fileName,
      file: file ?? this.file,
      copies: copies ?? this.copies,
      color: color ?? this.color,
      pageSize: pageSize ?? this.pageSize,
      comments: comments ?? this.comments,
    );
  }
}