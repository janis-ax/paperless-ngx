import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { PaperlessDocument, PaperlessDocumentPart } from '../data/paperless-document';
import { SplitMergeMetadata, SplitMergeRequest } from '../data/split-merge-request';

@Injectable({
  providedIn: 'root'
})
export class SplitMergeService {

  // this also needs to incorporate pages, if we want to support that.
  private documents: PaperlessDocument[] = []

  constructor(private http: HttpClient) { }

  addDocument(document: PaperlessDocument, atIndex?: number) {
    if (atIndex !== undefined) this.documents.splice(atIndex, 0, document)
    else this.documents.push(document)
  }

  addDocuments(documents: PaperlessDocument[]) {
    this.documents = this.documents.concat(documents)
  }

  removeDocument(document: PaperlessDocument, atIndex?: number) {
    if (!atIndex) atIndex = this.documents.indexOf(document)
    this.documents.splice(atIndex, 1)
  }

  reduceDocumentsTo(size: number) {
    if (this.documents.length > size) this.documents.length = size
  }

  getDocuments() {
    return this.documents
  }

  hasDocuments(): boolean {
    return this.documents.length > 0
  }

  clear() {
    this.documents = []
  }

  setDocumentPages(d: PaperlessDocument, index: number, pages: number[]) {
    (this.documents[index] as PaperlessDocumentPart).pages = pages.length > 0 ? pages : null
  }

  splitDocument(d: PaperlessDocument, index: number, secondPages: number[]) {
    const firstPages = []
    for (let page = 1; page < secondPages[0]; page++) {
      firstPages.push(page)
    }
    (this.documents[index] as PaperlessDocumentPart).pages = firstPages
    this.documents.splice(index + 1, 0, { is_separator: true })
    let d2 = { ...d }
    d2.pages = secondPages
    this.documents.splice(index + 2, 0, d2)
  }

  executeSplitMerge(preview: boolean, delete_source: boolean, metadata: SplitMergeMetadata): Observable<string[]> {
    let request: SplitMergeRequest = {
      delete_source: delete_source,
      preview: preview,
      metadata: metadata,
      split_merge_plan: [
        this.documents.map(d => { return {document: d.id, pages: (d as PaperlessDocumentPart).pages?.join(',')} })
      ]
    }
    return this.http.post<string[]>(`${environment.apiBaseUrl}split_merge/`, request)
  }

  getPreviewUrl(previewKey: string) {
    return `${environment.apiBaseUrl}split_merge/${previewKey}/`
  }

}
