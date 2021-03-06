import { Component, OnInit } from '@angular/core';
import { Subscription, timestamp } from 'rxjs';
import { ImageEntity } from '../imageEntity/imageEntity.model';
import { ImageEntityApiService } from '../imageEntity/imageEntity-api.service';
import { HttpClient } from '@angular/common/http';
import { Options } from '@angular-slider/ngx-slider';
@Component({
  selector: 'app-image-display',
  templateUrl: './image-display.component.html',
  styleUrls: ['./image-display.component.css']
})
export class ImageDisplayComponent implements OnInit {

  imagesListSubs: Subscription = Subscription.EMPTY;
  imagesList: ImageEntity[] = [];

  imageToShow: any = null;

  accuracy: number = 60;
  accuracyOptions: Options = {
    floor: 0,
    ceil: 100
  };

  useRaw = false

  qualityChanged(value: boolean){
    this.useRaw = value;
    console.log("Quality field changed to " + this.useRaw)
  }

  search: string = ""
  searchChanged(value: string){
    console.log("Search field changed to " + value)
    this.searchImages(value)
    
    this.imageToShow = null;
    this.search = value;
  }

  getPath(file: string): string{
    if (this.useRaw){
      return "images/raw/" + file;
    } else {
      return "images/cnn/" + file;
    }
  }

  accuracyEvent() {
    if (this.imageToShow != null) {
      this.getImagesLike(this.imageToShow, this.accuracy, this.maxRecommendations)
    }
  }

  maxRecommendations: number = 10;
  maxRecommendationsChanged(){
    this.getImagesLike(this.imageToShow, this.accuracy, this.maxRecommendations)
  }

  constructor(private imagesApi: ImageEntityApiService, private http: HttpClient){
    this.getAllImages();
  }

  getAllImages(){
    this.imagesListSubs = this.imagesApi
    .getImageEntities()
    .subscribe(res => {
        this.imagesList = res;
      },
      console.error
    );

    this.imageToShow = null;
    this.search = "";
  }

  getImagesLike(image: ImageEntity, accuracy: number, max: number){
    this.imagesListSubs = this.imagesApi
    .getImageEntitiesLike(image, accuracy, max)
    .subscribe(res => {
        this.imagesList = res;

        this.imagesList.unshift(this.imageToShow)
      },
      console.error
    );
  }

  searchImages(query: string){
    this.imagesListSubs = this.imagesApi
    .searchImageEntities(query)
    .subscribe(res => {
        this.imagesList = res;
      },
      console.error
    );
  }

  clickedImage(image: ImageEntity){
    console.log("Clicked on image: " + image.filename);
    this.getImagesLike(image, this.accuracy, this.maxRecommendations);

    this.imageToShow = image;
    this.search = "";
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
