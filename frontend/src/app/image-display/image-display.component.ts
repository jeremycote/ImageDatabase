import { Component, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';
import { ImageEntity } from '../imageEntity/imageEntity.model';
import { ImageEntityApiService } from '../imageEntity/imageEntity-api.service';

@Component({
  selector: 'app-image-display',
  templateUrl: './image-display.component.html',
  styleUrls: ['./image-display.component.css']
})
export class ImageDisplayComponent implements OnInit {

  imagesListSubs: Subscription = Subscription.EMPTY;
  imagesList: ImageEntity[] = [];

  constructor(private imagesApi: ImageEntityApiService){
    /*
    this.imagesListSubs = this.imagesApi
    .getExams()
    .subscribe(res => {
        this.imagesList = res;
      },
      console.error
    );
    */
  }
  ngOnInit() {
    this.imagesListSubs = this.imagesApi
      .getExams()
      .subscribe(res => {
          this.imagesList = res;
        },
        console.error
      );
  }

  ngOnDestroy() {
    this.imagesListSubs.unsubscribe();
  }
}
