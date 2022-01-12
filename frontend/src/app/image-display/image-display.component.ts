import { Component, OnInit } from '@angular/core';
import { Subscription, Observable, map } from 'rxjs';
import { ImageEntity } from '../imageEntity/imageEntity.model';
import { ImageEntityApiService } from '../imageEntity/imageEntity-api.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-image-display',
  templateUrl: './image-display.component.html',
  styleUrls: ['./image-display.component.css']
})
export class ImageDisplayComponent implements OnInit {

  imagesListSubs: Subscription;
  imagesList: ImageEntity[] = [];

  imageToShow:any;
  myURL:any

  constructor(private imagesApi: ImageEntityApiService, private http: HttpClient){
    this.imagesListSubs = this.imagesApi
    .getImageEntities()
    .subscribe(res => {
        this.imagesList = res;
      },
      console.error
    );
  }

  ngOnInit() {
    /*
    this.getImage(this.myURL).subscribe(data => {
      this.createImageFromBlob(data);
    }, error => {
      console.log("Error occured",error);
    });
    */
  }

  ngOnDestroy() {
    this.imagesListSubs.unsubscribe();
  }
/*
  getImage(imageUrl: string): Observable<Blob> {
      return this.http.get(imageUrl, { responseType: "blob"})
  }

  createImageFromBlob(image: Blob) {
   let reader = new FileReader(); //you need file reader for read blob data to base64 image data.
   reader.addEventListener("load", () => {
      this.imageToShow = reader.result; // here is the result you got from reader
   }, false);

   if (image) {
      reader.readAsDataURL(image);
   }
  }
  */
}
