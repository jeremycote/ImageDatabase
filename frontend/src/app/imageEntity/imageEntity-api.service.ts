import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import { throwError, Observable, catchError } from 'rxjs';
import {API_URL} from '../env';
import {ImageEntity} from './imageEntity.model';

@Injectable()
export class ImageEntityApiService {

  constructor(private http: HttpClient) {
  }

  handleError(error: HttpErrorResponse) {

    //throwError instead of Observable.throw
     return throwError(error.error.message ||"Server Error");
 };

  // GET list of public, future events
  getImageEntities(): Observable<ImageEntity[]> {
    console.log("getting image entities")
    return this.http.get<ImageEntity[]>(`${API_URL}/images`)
      .pipe(catchError(this.handleError))
  }

  getImageEntitiesLike(image: ImageEntity, accuracy: number, max: number): Observable<ImageEntity[]> {
    console.log("getting image entities like " + image.filename + " using id " + image.id)
    return this.http.get<ImageEntity[]>(`${API_URL}/similar_to/` + image.id + "/" + accuracy + "/" + max)
      .pipe(catchError(this.handleError))
  }

  searchImageEntities(query: string, category: string): Observable<ImageEntity[]> {
    console.log("searching image entities for " + query)
    return this.http.get<ImageEntity[]>(`${API_URL}/search/` + query + "/" + category)
      .pipe(catchError(this.handleError))
  }
}